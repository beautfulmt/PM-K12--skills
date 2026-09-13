#!/usr/bin/env python3
"""按项目的按需启动器：收到浏览器请求后在后台拉起导出服务。

这是「点一键导出/一键复制全文就自动起服务」背后的那一环。浏览器自己没法启动
进程，所以必须有个东西在 launcher_port 上应答——而那个东西就是 launchd 本身。

两种运行形态：
  * **socket 激活（macOS，默认）**：launchd 持有监听套接字，本进程只在真有请求
    时被拉起，处理完空闲一会儿就自退。空闲时项目没有任何常驻进程，端口却照样通。
    套接字由 launch_activate_socket() 交过来，所以这种形态下**不能自己 bind**。
  * **独立运行（回退）**：手动 `python3 scripts/prototype_launcher.py` 时拿不到
    launchd 的套接字，就自己 bind launcher_port，行为与旧版一致。

与 3.0 的关键差别：
  * label 按项目区分（com.pm-workflow.launcher.<project_id>），一台机器可同时
    服务多个项目；3.0 用的是全局唯一 label，后装的会顶掉先装的。
  * 配置按请求读取而不是模块导入期读取，因此项目未初始化时不会整个进程起不来。
"""
import ctypes
import ctypes.util
import json
import os
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pm_launchagent  # noqa: E402
from pm_bootstrap import ensure_serving  # noqa: E402
from pm_launchagent import IDLE_EXIT_SECONDS, SOCKET_NAME  # noqa: E402
from pm_runtime import cors_response_origin, ensure_config, origin_allowed, probe_health, valid_token  # noqa: E402

PROJECT_DIR = Path(os.environ.get("PROTOTYPE_PROJECT_DIR")
                   or Path(__file__).resolve().parent.parent).resolve()


def launch(config):
    state = probe_health(config["port"])
    if state:
        if state.get("project_id") != config["project_id"]:
            raise RuntimeError("端口被其他项目的服务占用")
        if state.get("read_only"):
            raise RuntimeError("当前服务为只读模式")
        return "already-running"
    result, _config = ensure_serving(PROJECT_DIR, background=True, verbose=False)
    return "launched" if result == "launched" else str(result)


class Handler(BaseHTTPRequestHandler):
    def config(self):
        # 每次请求都重读：端口可能因冲突自愈换过，token 可能被重新初始化过。
        if not hasattr(self, "_config"):
            self._config = ensure_config(PROJECT_DIR)
        return self._config

    def allowed_origin(self, config):
        origin = self.headers.get("Origin")
        return origin_allowed(origin, config["launcher_port"]) or origin in (
            f"http://127.0.0.1:{config['port']}", f"http://localhost:{config['port']}")

    def reply(self, data, code=200, config=None):
        raw = json.dumps(data).encode()
        self.send_response(code)
        origin = self.headers.get("Origin")
        if origin and config and self.allowed_origin(config):
            self.send_header("Access-Control-Allow-Origin", cors_response_origin(origin))
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-PM-Project, X-PM-Token")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        try:
            config = self.config()
        except Exception:
            self.reply({}, 403)
            return
        self.reply({}, 200 if self.allowed_origin(config) else 403, config)

    def do_POST(self):
        try:
            config = self.config()
        except Exception as error:
            self.reply({"error": str(error)}, 400)
            return
        if (self.path != "/api/launch" or not self.allowed_origin(config)
                or not valid_token(self.headers, config)):
            self.reply({"error": "项目身份校验失败"}, 403, config)
            return
        try:
            self.reply({"ok": True, "status": launch(config),
                        "project_id": config["project_id"]}, 200, config)
        except Exception as error:
            self.reply({"error": str(error)}, 400, config)

    def log_message(self, fmt, *args):  # 降噪：常驻进程不需要逐条 access log
        pass


def launchd_socket(name=SOCKET_NAME):
    """取 launchd 交过来的监听套接字 fd；不在 launchd 下运行时返回 None。

    非 launchd 环境下 launch_activate_socket 返回 ESRCH(3)，属于预期情况，
    不是错误——调用方据此回退到自己 bind。
    """
    try:
        lib = ctypes.CDLL(ctypes.util.find_library("System") or "/usr/lib/libSystem.dylib")
        fn = lib.launch_activate_socket
    except (OSError, AttributeError):
        return None  # 非 macOS，或系统不提供该符号
    fn.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
                   ctypes.POINTER(ctypes.c_size_t)]
    fn.restype = ctypes.c_int
    fds = ctypes.POINTER(ctypes.c_int)()
    count = ctypes.c_size_t(0)
    if fn(name.encode(), ctypes.byref(fds), ctypes.byref(count)) != 0 or count.value < 1:
        return None
    return fds[0]


class InheritedServer(HTTPServer):
    """用 launchd 已建好的套接字，跳过 bind/listen。

    自己 bind 会直接撞 EADDRINUSE——那个端口正被 launchd 占着。
    """

    def __init__(self, fd, handler):
        super().__init__(("127.0.0.1", 0), handler, bind_and_activate=False)
        self.socket.close()
        # dup 一份：原 fd 的所有权在 launchd 那边，不该被 Python 的 GC 关掉。
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=os.dup(fd))
        self.server_address = self.socket.getsockname()


if __name__ == "__main__":
    try:
        CONFIG = ensure_config(PROJECT_DIR)
    except Exception as error:
        print(f"启动器无法读取项目配置，已退出：{error}", file=sys.stderr)
        sys.exit(0)  # 不用非 0 退出，否则 launchd 的 KeepAlive 会无限重启

    INHERITED = launchd_socket()
    if INHERITED is None:
        # 独立运行：自己 bind，长驻不自退（用户是手动起的，退了会让人意外）
        HTTPServer(("127.0.0.1", int(CONFIG["launcher_port"])), Handler).serve_forever()
    else:
        # 本进程就是那个 launchd job：任何路径都不许再去重新注册它（会自杀，详见
        # pm_launchagent.IN_LAUNCHD_JOB）。必须赶在起服务之前置上。
        pm_launchagent.IN_LAUNCHD_JOB = True
        SERVER = InheritedServer(INHERITED, Handler)
        # 空闲即退，这样「零常驻」才成立；下次请求由 launchd 再拉起。
        SERVER.timeout = IDLE_EXIT_SECONDS
        SERVER.handle_timeout = lambda: sys.exit(0)
        while True:
            SERVER.handle_request()
