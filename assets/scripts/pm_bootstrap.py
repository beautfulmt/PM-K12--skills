#!/usr/bin/env python3
"""把「确保服务可用」收敛成唯一代码路径，供 mac .command / Windows .bat / 后台 launcher 共用。

对外只有四个入口：
  ensure_config(root)                      读不到配置就创建（在 pm_runtime 里）
  ensure_runtime(...)   -> (python, engine)  共享 venv + 浏览器引擎，幂等
  ensure_serving(root, ...)                 前台占用当前窗口 / 后台脱离终端
  doctor(root)                              一次打印全部环境事实，用于远程排查

跨平台注意点（都是踩过的）：
  * Windows 没有 python3 命令；py -3 是官方启动器，但微软商店的 alias stub 会
    打开商店且不可靠地返回 0，所以解释器探测只认正向哨兵输出，不看退出码。
  * 不用 os.execve：Windows 上它是 CreateProcess + 父进程立即退出，会让 .bat
    窗口一闪即关，也让 launcher 的 poll() 判活永久失效。改成显式两段式 spawn。
  * 子进程一律强制 UTF-8：服务端打印中文横幅，stdout 被重定向到日志文件后
    Python 会改用 locale 编码，英文区 Windows 是 cp1252，启动即 UnicodeEncodeError。
  * venv 放用户目录而非项目目录：项目常在 OneDrive/iCloud 里，会引发同步风暴、
    os.replace 的 PermissionError，以及 Windows MAX_PATH 260 超限。
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pm_runtime import (VERSION, atomic_write, ensure_config, probe_health,  # noqa: E402
                        reroll_ports)

PLAYWRIGHT_VERSION = os.environ.get("PM_PLAYWRIGHT_VERSION", "1.60.0")
MIN_PYTHON = (3, 9)
SENTINEL = "PMPY-OK"
_PROBE = "import sys;print('{}',sys.version_info[0],sys.version_info[1])".format(SENTINEL)
# 引擎优先级：优先复用系统已装的浏览器（零下载），都没有才回落 Playwright 自带 Chromium。
# None 代表自带 Chromium。Windows 上 Edge 是系统自带，命中率最高。
_ENGINE_ORDER = {"nt": ["msedge", "chrome", None], "darwin": ["chrome", "msedge", None]}
_ENGINE_PROBE = """
import sys
from playwright.sync_api import sync_playwright
channel = sys.argv[1] or None
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, channel=channel) if channel \\
        else p.chromium.launch(headless=True)
    browser.close()
print("PMENGINE-OK")
"""


# ---------------------------------------------------------------- 共享目录

def shared_dir():
    """跨项目共享的运行时目录——里面没有任何项目相关内容。"""
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or Path.home() / "AppData/Local"
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share"
    return Path(base) / "pm-workflow"


def venv_dir():
    return shared_dir() / "venv"


def venv_python():
    sub = "Scripts/python.exe" if os.name == "nt" else "bin/python"
    return venv_dir() / sub


def _state_path():
    return shared_dir() / "state.json"


def read_state():
    """引擎/版本等与机器绑定、与项目无关的事实，跟着共享 venv 一起存。"""
    try:
        state = json.loads(_state_path().read_text(encoding="utf-8"))
        return state if isinstance(state, dict) else {}
    except (OSError, ValueError):
        return {}


def write_state(**updates):
    state = read_state()
    state.update(updates)
    atomic_write(_state_path(), json.dumps(state, ensure_ascii=False, indent=2))
    return state


def launch_engine():
    """服务端截图时用的 channel；None 表示 Playwright 自带 Chromium。"""
    return read_state().get("engine") or None


# ---------------------------------------------------------------- 解释器

def _probe_interpreter(command):
    """只认正向哨兵输出：商店 stub 会返回 0 但不打印任何东西。"""
    try:
        result = subprocess.run(list(command) + ["-c", _PROBE],
                                capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    for line in (result.stdout or "").splitlines():
        parts = line.strip().split()
        if len(parts) == 3 and parts[0] == SENTINEL:
            try:
                version = (int(parts[1]), int(parts[2]))
            except ValueError:
                continue
            if version >= MIN_PYTHON:
                return list(command), version
    return None


def interpreter_candidates():
    if os.name == "nt":
        return [["py", "-3"], ["python"], ["python3"]]
    return [["python3"], ["python"]]


def find_python(include_self=True):
    """返回 (命令列表, 版本元组)；找不到返回 None。"""
    if include_self:
        found = _probe_interpreter([sys.executable])
        if found:
            return found
    for candidate in interpreter_candidates():
        found = _probe_interpreter(candidate)
        if found:
            return found
    return None


# ---------------------------------------------------------------- 子进程环境

def child_env(**extra):
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # stdout 重定向进 service.log 后会变成块缓冲（~8KB），进程被 kill 时整段丢失——
    # 也就是「详见 service.log」最需要它的时候日志恰好是空的。
    env["PYTHONUNBUFFERED"] = "1"
    for key, value in extra.items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = str(value)
    return env


def _spawn_kwargs(background):
    """后台模式脱离当前终端：POSIX 用新会话，Windows 用无窗口 + 独立进程组。"""
    if not background:
        return {}
    if os.name == "nt":
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
        flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
        return {"creationflags": flags}
    return {"start_new_session": True}


# ---------------------------------------------------------------- 运行时安装

def _run(command, description, env=None):
    result = subprocess.run(command, env=env or child_env())
    if result.returncode:
        raise RuntimeError(f"{description}失败（退出码 {result.returncode}）")


_VERSION_PROBE = ("from importlib.metadata import version;"
                  "import playwright;print(version('playwright'))")


def _playwright_installed(python):
    """playwright 包没有 __version__ 属性，只能问包元数据。

    这里一并 import playwright：光有元数据不代表能 import（装到一半、
    site-packages 被清过等情况都会元数据在、模块不在）。
    """
    result = subprocess.run([str(python), "-c", _VERSION_PROBE],
                            capture_output=True, text=True, env=child_env())
    return (result.stdout or "").strip() if result.returncode == 0 else None


def _probe_engine(python, channel):
    result = subprocess.run([str(python), "-c", _ENGINE_PROBE, channel or ""],
                            capture_output=True, text=True, env=child_env(), timeout=180)
    return "PMENGINE-OK" in (result.stdout or ""), (result.stderr or "").strip()


def detect_engine(python, allow_download=True, verbose=True):
    """按平台优先级探测可用引擎；系统浏览器都不可用时才下载自带 Chromium。"""
    order = _ENGINE_ORDER.get("nt" if os.name == "nt" else sys.platform, ["chrome", None])
    last_error = ""
    for channel in order:
        if channel is None:
            continue
        ok, error = _probe_engine(python, channel)
        if ok:
            if verbose:
                print(f"  ✅ 复用系统已装浏览器：{channel}（无需下载）")
            return channel
        last_error = error
    # 自带 Chromium：可能已经下载过，先直接试
    ok, error = _probe_engine(python, None)
    if ok:
        if verbose:
            print("  ✅ 使用 Playwright 自带 Chromium")
        return None
    if not allow_download:
        raise RuntimeError("没有可用的浏览器引擎，且当前不允许下载。"
                           f"最后一次错误：{(error or last_error)[:200]}")
    if verbose:
        print("  ⬇️  未发现可复用的系统浏览器，正在下载 Chromium（约 150MB，仅首次）…", flush=True)
    _run([str(python), "-m", "playwright", "install", "chromium"], "下载 Chromium")
    ok, error = _probe_engine(python, None)
    if not ok:
        raise RuntimeError("Chromium 下载后仍无法启动。"
                           "Linux 可能缺系统依赖（playwright install-deps）。"
                           f"错误：{error[:200]}")
    return None


def ensure_runtime(allow_download=True, verbose=True, force_install=False):
    """确保共享 venv + playwright + 可用引擎就位。幂等，返回 (venv_python, engine)。"""
    python = venv_python()
    if force_install or not python.exists():
        found = find_python()
        if not found:
            raise RuntimeError(
                "找不到可用的 Python 3.9+。\n"
                "  macOS：从 https://www.python.org/downloads/ 安装，或执行 brew install python\n"
                "  Windows：在应用商店或 https://www.python.org/downloads/ 安装，"
                "安装时请勾选「Add python.exe to PATH」")
        host_command = found[0]
        if not python.exists():
            if verbose:
                print(f"  📦 正在创建共享运行环境：{venv_dir()}", flush=True)
            venv_dir().parent.mkdir(parents=True, exist_ok=True)
            _run(host_command + ["-m", "venv", str(venv_dir())], "创建虚拟环境")
    if not python.exists():
        raise RuntimeError(f"虚拟环境创建后仍找不到解释器：{python}")

    installed = _playwright_installed(python)
    if force_install or installed != PLAYWRIGHT_VERSION:
        if verbose:
            print(f"  📦 正在安装 playwright=={PLAYWRIGHT_VERSION}", flush=True)
        try:
            _run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
                  "playwright==" + PLAYWRIGHT_VERSION], "安装 playwright")
        except RuntimeError:
            raise RuntimeError(
                "安装 playwright 失败。若公司网络需要代理，请先设置后重试：\n"
                "  macOS：export HTTPS_PROXY=http://代理地址:端口\n"
                "  Windows：set HTTPS_PROXY=http://代理地址:端口")

    engine = read_state().get("engine", "__unset__")
    if force_install or engine == "__unset__" or not _probe_engine(python, engine or None)[0]:
        engine = detect_engine(python, allow_download=allow_download, verbose=verbose)
        write_state(engine=engine, playwright=PLAYWRIGHT_VERSION, version=VERSION,
                    python=str(python))
    return python, engine


# ---------------------------------------------------------------- 启动服务

def _server_script():
    return Path(__file__).resolve().parent / "prototype_server.py"


def held_by_own_launcher(config, port):
    """launcher_port bind 不上，但占用者是本项目自己的 LaunchAgent——这是正常状态。

    socket 激活下这个端口由 launchd 长期持有，那正是「空闲零进程、端口仍然通」的
    实现方式。只给 --doctor 用，用来把这种情况和真冲突区分开。
    """
    if sys.platform != "darwin":
        return False
    try:
        import pm_launchagent
        return pm_launchagent.registered_port(config) == int(port)
    except Exception:  # noqa: BLE001
        return False


def reserve_ports(root, config, attempts=8):
    """确认服务端口可 bind；被占则重推并回写配置，不永久占坑。

    **只看服务端口。** launcher_port 不归这里管，而且探它必然出错：它要么被
    launchd 长期持有（socket 激活），要么被独立运行的启动器自己持有——两种情况下
    「bind 不上」都是正常状态。更要命的是它已改成不随 salt 漂移（见 derive_ports），
    重抽根本换不掉它，一旦把它判成冲突就是 8 次空转后报「没抽到可用端口」。
    它真被外人占了的话，由启动器自己 bind 时报错，或注册时 bootstrap 失败暴露。
    """
    import socket
    for _ in range(attempts):
        with socket.socket() as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(("127.0.0.1", int(config["port"])))
                return config
            except OSError:
                pass
        config = reroll_ports(root, config)
    raise RuntimeError("连续多次都没抽到可用端口，请检查本机端口占用情况")


def ensure_serving(root, background=False, read_only=False, host="127.0.0.1",
                   open_browser=False, verbose=True, allow_download=True):
    """确保当前项目的服务在跑。

    前台：占用当前窗口，服务本体就是前台进程，⌃C 可停。
    后台：脱离终端，日志进 .pm-workflow/service.log。
    """
    root = Path(root).resolve()
    config = ensure_config(root)

    state = probe_health(config["port"])
    if state:
        if state.get("project_id") != config["project_id"]:
            raise RuntimeError(f"端口 {config['port']} 被其他项目的服务占用，请先停止它")
        if bool(state.get("read_only")) != bool(read_only):
            raise RuntimeError("已有服务的读写模式与本次请求不一致，请先停止它")
        if verbose:
            print(f"  ✅ 当前项目服务已在运行：http://127.0.0.1:{config['port']}")
        return "already-running", config

    if host not in ("127.0.0.1", "localhost", "::1") and not read_only:
        raise RuntimeError("局域网监听只允许 --read-only 模式")

    python, _engine = ensure_runtime(allow_download=allow_download, verbose=verbose)
    config = reserve_ports(root, config)

    env = child_env(PM_SERVER_HOST=host,
                    PM_READ_ONLY="1" if read_only else "0",
                    PM_OPEN_BROWSER="1" if (open_browser and not background) else None,
                    PROTOTYPE_PROJECT_DIR=str(root))
    command = [str(python), str(_server_script())]

    if not background:
        try:
            return subprocess.run(command, cwd=str(root), env=env).returncode, config
        except KeyboardInterrupt:
            return 0, config

    log_path = root / ".pm-workflow/service.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("ab") as stream:
        process = subprocess.Popen(command, cwd=str(root), env=env, stdout=stream,
                                   stderr=stream, stdin=subprocess.DEVNULL,
                                   **_spawn_kwargs(True))
    deadline = time.time() + 45
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"服务启动失败（退出码 {process.returncode}），"
                               f"详见 {log_path}")
        if probe_health(config["port"]):
            return "launched", config
        time.sleep(0.4)
    raise RuntimeError(f"服务启动超时，详见 {log_path}")


# ---------------------------------------------------------------- 体检

def _mark(ok):
    return "✅" if ok else "❌"


def doctor(root):
    """一次打印全部环境事实——远程排查时让对方截这一张图就够。"""
    root = Path(root).resolve()
    print("=" * 60)
    print(f"  PM Workflow 环境体检  v{VERSION}")
    print("=" * 60)
    print(f"  平台：{sys.platform} / os.name={os.name}")
    print(f"  项目：{root}")

    found = find_python()
    print(f"\n  {_mark(bool(found))} 解释器：" +
          (f"{' '.join(found[0])}  → Python {found[1][0]}.{found[1][1]}" if found
           else f"未找到 Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+"))
    print(f"      当前进程：{sys.executable}  ({sys.version.split()[0]})")

    python = venv_python()
    print(f"  {_mark(python.exists())} 共享运行环境：{venv_dir()}")
    if python.exists():
        installed = _playwright_installed(python)
        want = PLAYWRIGHT_VERSION
        print(f"  {_mark(installed == want)} playwright：{installed or '未安装'}（期望 {want}）")
        state = read_state()
        engine = state.get("engine", "__unset__")
        if engine == "__unset__":
            print("  ❌ 浏览器引擎：尚未探测")
        else:
            ok, error = _probe_engine(python, engine or None)
            label = engine or "Playwright 自带 Chromium"
            print(f"  {_mark(ok)} 浏览器引擎：{label}" + ("" if ok else f" — {error.splitlines()[0][:80]}"))
    else:
        print("  ❌ playwright：共享环境未创建，无法检查")

    config_file = root / ".pm-workflow/runtime.json"
    existed = config_file.is_file()
    try:
        config = ensure_config(root)  # 缺失时就地创建，所以下面的 ✅ 永远成立
    except Exception as error:
        print(f"\n  ❌ 运行配置不可用：{config_file}\n      {error}")
        return 1
    print(f"\n  ✅ 运行配置：{config_file}" + ("" if existed else "（本次新建）"))
    print(f"      项目标识：{config['project_id']}")
    import socket
    for key, label in (("port", "服务端口"), ("launcher_port", "启动器端口")):
        port = int(config[key])
        with socket.socket() as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(("127.0.0.1", port))
                free = True
            except OSError as error:
                free = False
                reason = str(error)
        if free:
            print(f"  ✅ {label} {port}：可用")
        elif held_by_own_launcher(config, port):
            # 不是冲突：socket 激活就是靠 launchd 长期占着这个端口实现的。
            print(f"  ✅ {label} {port}：由 launchd 持有（按需启动器正常工作中）")
        else:
            state = probe_health(port)
            if state and state.get("project_id") == config["project_id"]:
                print(f"  ✅ {label} {port}：本项目服务正在使用")
            elif key == "launcher_port":
                # 这个端口不会自愈（它固定不变），所以不能说「启动时会自动换端口」。
                print(f"  ⚠️  {label} {port}：被别的程序占用（{reason}）")
                print("      影响：点导出不会自动起服务。停掉占用方后重跑 "
                      "bash scripts/install_launcher.sh；期间双击启动入口照常可用。")
            else:
                print(f"  ⚠️  {label} {port}：被占用（{reason}）；启动时会自动换端口")

    entries = [("启动原型导出服务.command", os.name != "nt"),
               ("启动原型导出服务.bat", os.name == "nt")]
    print()
    for name, relevant in entries:
        path = root / name
        if not path.exists():
            print(f"  {'❌' if relevant else '  '} 启动入口 {name}：不存在")
        elif os.name != "nt" and name.endswith(".command"):
            executable = os.access(path, os.X_OK)
            print(f"  {_mark(executable)} 启动入口 {name}：" +
                  ("可执行" if executable else "缺少可执行权限，请运行 chmod +x"))
        else:
            print(f"  ✅ 启动入口 {name}：存在")

    if sys.platform == "darwin":
        import pm_launchagent
        registered, agent_port, matched, pid = pm_launchagent.status(config)
        if not registered:
            print("  ⚠️  按需启动器：未注册——点导出不会自动起服务，需要先双击启动入口。")
            print("      注册：bash scripts/install_launcher.sh")
        elif not matched:
            # plist 里的端口是写死的，端口自愈过就会错位。
            print(f"  ⚠️  按需启动器：登记的是端口 {agent_port}，当前配置是 "
                  f"{config['launcher_port']}——已错位，自动启动不生效。")
            print("      重新注册：bash scripts/install_launcher.sh")
        else:
            print(f"  ✅ 按需启动器：已注册（端口 {agent_port}，由 launchd 持有）")
            print("      启动器进程：" +
                  (f"PID {pid}" if pid else "无（空闲即退，属正常——端口仍然通）"))

    proxies = {k: v for k, v in os.environ.items()
               if k.upper() in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")}
    print(f"\n  代理环境变量：{proxies or '（无）'}")
    if proxies and not any(k.upper() == "NO_PROXY" for k in proxies):
        print("      提示：已设置代理但没有 NO_PROXY；本服务的本机请求已强制绕过代理。")
    print("=" * 60)
    return 0
