#!/usr/bin/env python3
"""macOS 按需启动器的 LaunchAgent 注册（socket 激活版）。

为什么不用 RunAtLoad + KeepAlive
--------------------------------
上一版装的是一个真常驻进程：开机就起、退出就重拉，每个项目一个。给自己用尚可，
但这个 skill 是要分享出去的——在别人机器上悄悄留下常驻进程是不合适的，所以当初
把它设成了「默认不装」。结果是**自动启动这条链路等于没有**：浏览器点导出时
去叫 launcher_port，那儿没人应答，于是永远弹「请双击启动脚本」。

socket 激活解决的正是这个两难。plist 里只给 Sockets，不给 RunAtLoad、不给
KeepAlive：**端口由 launchd 自己持有**。空闲时本项目没有任何进程在跑，但端口照样
是通的；浏览器一连上来，launchd 才把 prototype_launcher.py 拉起来，它起完服务就
自退。既是自动启动，又没有常驻进程，所以可以默认装。

plist 里写死了端口，而端口是会自愈的（bind 冲突时换一对），所以 sync() 必须在
端口变化后被调用，否则 launchd 会守着一个没人用的旧端口。
"""
import os
import plistlib
import subprocess
import sys
from pathlib import Path

SOCKET_NAME = "Listeners"
# 空闲多久自退。给足冗余吸收客户端重试（它启动后会轮询健康检查最多 45s），
# 又短到「用完即走」仍然成立。
IDLE_EXIT_SECONDS = 120

# 由 prototype_launcher 在 socket 激活分支里置 True。
# 重新注册要先 launchctl bootout，而 bootout 会杀掉这个 job 的进程——如果那正是
# 当前进程，就等于自杀：请求得不到回应，注册也留在半路（bootout 成功、bootstrap
# 没跑成），「点导出自动起服务」从此彻底失效，只能手动重装。实测过一次，故有此标志。
IN_LAUNCHD_JOB = False


def supported():
    return sys.platform == "darwin"


def label(config):
    # 按项目区分：3.0 用全局唯一 label，一台机器只能服务一个项目，后装的顶掉先装的。
    return "com.pm-workflow.launcher." + config["project_id"]


def plist_path(config):
    return Path.home() / "Library/LaunchAgents" / (label(config) + ".plist")


def _domain():
    return "gui/" + str(os.getuid())


def _interpreter(explicit=None):
    """选一个写进 plist 的解释器路径。

    不能用共享 venv 里的那个：venv 会被 --install 重建，路径失效后 launchd 只会
    反复拉起失败。挑系统级的 python3。
    """
    if explicit:
        return str(explicit)
    exe = Path(sys.executable)
    in_venv = (exe.parent.parent / "pyvenv.cfg").is_file() or "pm-workflow" in exe.parts
    if in_venv:
        for candidate in ("/opt/homebrew/bin/python3", "/usr/local/bin/python3",
                          "/usr/bin/python3"):
            if Path(candidate).is_file():
                return candidate
    return str(exe)


def registered_port(config):
    """plist 里当前登记的端口；未注册返回 None。"""
    path = plist_path(config)
    if not path.is_file():
        return None
    try:
        data = plistlib.loads(path.read_bytes())
        sock = (data.get("Sockets") or {}).get(SOCKET_NAME) or {}
        return int(sock.get("SockServiceName"))
    except (OSError, ValueError, TypeError, KeyError):
        return None


def installed(config):
    return plist_path(config).is_file()


def install(root, config, python=None):
    """写 plist 并注册。返回 (ok, 说明文字)。"""
    if not supported():
        return False, "常驻启动器只支持 macOS"
    root = Path(root).resolve()
    launcher = root / "scripts/prototype_launcher.py"
    if not launcher.is_file():
        return False, f"找不到 {launcher}"

    path = plist_path(config)
    logs = Path.home() / "Library/Logs/pm-workflow" / config["project_id"]
    try:
        logs.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

    settings = {
        "Label": label(config),
        # 直接指向项目里的脚本，不复制副本：副本在 skill 升级后不会同步，
        # 会变成一份悄悄跑着的旧代码。
        "ProgramArguments": [_interpreter(python), str(launcher)],
        "EnvironmentVariables": {
            "PROTOTYPE_PROJECT_DIR": str(root),
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUNBUFFERED": "1",
        },
        # 没有 RunAtLoad、没有 KeepAlive：完全靠下面这个套接字按需拉起。
        "Sockets": {
            SOCKET_NAME: {
                "SockNodeName": "127.0.0.1",
                "SockServiceName": str(config["launcher_port"]),
                "SockType": "stream",
                "SockFamily": "IPv4",
            }
        },
        # 无 KeepAlive 时不存在崩溃自旋的风险，所以把节流压到最低，
        # 保证连续两次点导出都能立刻被拉起。
        "ThrottleInterval": 1,
        "StandardOutPath": str(logs / "launcher.log"),
        "StandardErrorPath": str(logs / "launcher-error.log"),
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(plistlib.dumps(settings))
    except OSError as error:
        return False, f"写 plist 失败：{error}"

    subprocess.run(["launchctl", "bootout", _domain(), str(path)], capture_output=True)
    result = subprocess.run(["launchctl", "bootstrap", _domain(), str(path)],
                            capture_output=True, text=True)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()[:200]
        return False, f"launchctl bootstrap 失败：{detail}"
    return True, f"{label(config)} 端口 {config['launcher_port']}"


def uninstall(config):
    if not supported():
        return False, "常驻启动器只支持 macOS"
    path = plist_path(config)
    subprocess.run(["launchctl", "bootout", _domain(), str(path)], capture_output=True)
    try:
        if path.is_file():
            path.unlink()
    except OSError as error:
        return False, f"删除 plist 失败：{error}"
    return True, label(config)


def sync(root, config, python=None):
    """端口变化后把注册对齐。**从不主动安装**——没注册过就什么都不做。

    正常情况下不该被触发：启动器端口已改成不随 salt 漂移（见 derive_ports）。
    留着是为了兜住历史配置——3.2 之前重抽过端口的项目，升级后登记端口可能对不上。
    """
    if not supported() or not installed(config) or IN_LAUNCHD_JOB:
        return None
    if registered_port(config) == int(config["launcher_port"]):
        return None
    ok, detail = install(root, config, python=python)
    return ok, detail


def running_pid(config):
    """当前是否有启动器进程在跑，问 launchd 而不是探端口。

    探端口会**触发**一次 socket 激活——即把要观测的进程亲手拉起来，然后
    报告「它在跑」。而且启动器只认 POST /api/launch，没有健康检查接口。
    """
    if not supported():
        return None
    result = subprocess.run(["launchctl", "list", label(config)],
                            capture_output=True, text=True)
    if result.returncode:
        return None
    for line in result.stdout.splitlines():
        if '"PID"' in line:
            digits = "".join(ch for ch in line.split("=")[-1] if ch.isdigit())
            return int(digits) if digits else None
    return None


def status(config):
    """给 --doctor 用：(已注册?, 登记端口, 端口是否与配置一致, 当前 PID)"""
    if not supported():
        return False, None, True, None
    port = registered_port(config)
    return (installed(config), port, port == int(config["launcher_port"]),
            running_pid(config))
