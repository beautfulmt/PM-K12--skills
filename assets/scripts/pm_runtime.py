"""Project-scoped configuration shared by the preview server, launcher and bootstrap.

设计要点：
  * 端口由 project_id 确定性推导到 20000-32767，避开 OS 临时端口段（49152+），
    那一段既会被系统派给出站连接，在 Windows 上还有 Hyper-V/WSL/Docker 的保留块。
  * 端口可自愈：bind 失败时换 salt 重新推导并回写配置，不会永久占坑。
  * ensure_config() 是 create-or-load，缺配置时创建而不是抛错——任何人 clone 一个
    项目仓（.pm-workflow/ 被 gitignore）都不该看到 traceback。
"""
import hashlib
import json
import os
import secrets
import tempfile
from pathlib import Path
from urllib.request import ProxyHandler, build_opener

VERSION = "3.3.0"
PORTS_SCHEME = "deterministic-v2"
PORT_FLOOR = 20000
PORT_SPAN = 12767  # 20000..32766，+1 后仍不超过 32767


def atomic_write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def config_path(root):
    return Path(root).resolve() / ".pm-workflow/runtime.json"


def derive_ports(project_id, salt=0):
    """由项目标识确定性推导服务端口与启动器端口；salt 用于 bind 冲突时换一个。

    **salt 只作用于服务端口，启动器端口固定不变。** 后者被写死在 macOS 的
    LaunchAgent plist 里，而换 plist 端口只能 bootout + bootstrap——bootout 会
    连带杀掉正在处理这次请求的启动器进程自己。让它永不漂移，这个竞态就不存在。
    真正会跟别的应用撞车的本来也只有服务端口。
    """
    launcher = PORT_FLOOR + int.from_bytes(
        hashlib.sha256(f"{project_id}:0".encode()).digest()[:4], "big") % PORT_SPAN + 1
    seed = hashlib.sha256(f"{project_id}:{salt}".encode()).digest()
    port = PORT_FLOOR + int.from_bytes(seed[:4], "big") % PORT_SPAN
    if port == launcher:  # 重抽时正好撞上固定的启动器端口，往后挪一格
        port = PORT_FLOOR + (port + 1 - PORT_FLOOR) % PORT_SPAN
    return port, launcher


def _browser_config(config):
    return {
        "projectId": config["project_id"],
        "token": config["token"],
        "server": "http://127.0.0.1:" + str(config["port"]),
        "launcher": "http://127.0.0.1:" + str(config["launcher_port"]),
    }


def write_browser_config(root, config):
    """浏览器侧配置，随端口变化重写，被 prototype-export-client.js 动态加载。"""
    atomic_write(Path(root).resolve() / "scripts/pm-runtime-config.js",
                 "window.PM_RUNTIME = " + json.dumps(_browser_config(config)) + ";\n")


def save_config(root, config):
    root = Path(root).resolve()
    path = config_path(root)
    config["version"] = VERSION
    atomic_write(path, json.dumps(config, ensure_ascii=False, indent=2))
    try:
        path.chmod(0o600)  # 内含项目 token；Windows 上该位无意义，失败不阻断
    except OSError:
        pass
    write_browser_config(root, config)
    return config


def ensure_config(root):
    """读不到就创建；结构过期就就地升级。永不因缺文件抛错。"""
    root = Path(root).resolve()
    path = config_path(root)
    config = {}
    if path.is_file():
        try:
            config = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            config = {}  # 配置损坏时重建，比让每个入口都 traceback 好
    if not isinstance(config, dict):
        config = {}

    moved = config.get("root") != str(root)
    if moved or not config.get("project_id"):
        # 目录被移动过：project_id 由绝对路径派生，必须重算，否则端口/身份都对不上
        config["root"] = str(root)
        config["project_id"] = hashlib.sha256(str(root).encode()).hexdigest()[:16]
        config.pop("ports_scheme", None)
    if not config.get("token"):
        config["token"] = secrets.token_urlsafe(32)
    if config.get("ports_scheme") != PORTS_SCHEME or not config.get("port"):
        # 老配置的端口抽自 OS 临时端口段，迁到确定性区间
        config["port"], config["launcher_port"] = derive_ports(config["project_id"])
        config["port_salt"] = 0
        config["ports_scheme"] = PORTS_SCHEME
    return save_config(root, config)


def load_config(root):
    """只读加载；供已初始化的场景使用，缺文件时给出可执行的指引而非裸 traceback。"""
    path = config_path(root)
    if not path.is_file():
        raise RuntimeError(
            "尚未初始化项目运行配置。请双击项目根目录的「启动原型导出服务」"
            "（Windows 为 .bat），它会自动创建配置并启动服务。")
    config = json.loads(path.read_text(encoding="utf-8"))
    if Path(config["root"]).resolve() != Path(root).resolve():
        raise RuntimeError(
            "项目目录已移动。请双击项目根目录的「启动原型导出服务」（Windows 为 .bat）重新初始化。")
    return config


def reroll_ports(root, config):
    """bind 冲突后换一对端口并回写，返回新配置。

    这里是全局唯一改动端口的地方，所以 LaunchAgent 的同步也放在这里：plist 里的
    端口是写死的，漏同步一次，launchd 就会守着一个没人访问的旧端口，
    「点导出自动起服务」静默失效。放在调用点上同步的话，每新增一条自愈路径
    都得记得补一次——迟早漏。
    """
    config["port_salt"] = int(config.get("port_salt", 0)) + 1
    config["port"], config["launcher_port"] = derive_ports(config["project_id"], config["port_salt"])
    config["ports_scheme"] = PORTS_SCHEME
    config = save_config(root, config)
    try:
        import pm_launchagent
        pm_launchagent.sync(root, config)  # 没注册过则什么都不做
    except Exception:  # noqa: BLE001 — 同步失败不该拖垮启动，doctor 会报错位
        pass
    return config


def local_opener():
    """127.0.0.1 的健康检查必须绕开代理——urllib 默认也会走 HTTP_PROXY，
    代理返回的 HTML 会让 json 解析失败，从而误判“服务没在跑”并重复启动。"""
    return build_opener(ProxyHandler({}))


def probe_health(port, timeout=1.5):
    """返回服务自报的状态；连不上或不是本服务时返回 None。"""
    try:
        with local_opener().open(f"http://127.0.0.1:{port}/api/health", timeout=timeout) as response:
            state = json.load(response)
        return state if isinstance(state, dict) else None
    except Exception:
        return None


def origin_allowed(origin, port):
    return origin in (None, "null", "http://127.0.0.1:" + str(port), "http://localhost:" + str(port))


def valid_token(headers, config):
    return (headers.get("X-PM-Project") == config["project_id"] and
            secrets.compare_digest(headers.get("X-PM-Token", ""), config["token"]))
