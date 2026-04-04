import argparse
import os
import socket
import threading
import time

try:
    from flask import Flask, jsonify, request
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "ShikiDashboard Resource Monitor Agent requires Flask. Install it with: pip install flask"
    ) from exc

try:
    import psutil
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "ShikiDashboard Resource Monitor Agent requires psutil. Install it with: pip install psutil"
    ) from exc


class ResourceMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self._ready = threading.Event()
        self._stats = self._empty_stats()
        self._thread = None

    def _empty_stats(self):
        return {
            "available": True,
            "error": None,
            "cpu_percent": None,
            "memory_percent": None,
            "memory_used_bytes": None,
            "memory_total_bytes": None,
            "upload_bps": None,
            "download_bps": None,
            "sampled_at": None,
            "hostname": socket.gethostname(),
        }

    def ensure_started(self):
        if self._thread:
            return
        self._thread = threading.Thread(target=self._run, daemon=True, name="remote-host-agent-monitor")
        self._thread.start()

    def _run(self):
        psutil.cpu_percent(interval=None)
        last_sample_time = time.time()
        last_net = psutil.net_io_counters()
        while True:
            now = time.time()
            memory = psutil.virtual_memory()
            net = psutil.net_io_counters()
            elapsed = max(now - last_sample_time, 0.001)
            snapshot = {
                "available": True,
                "error": None,
                "cpu_percent": round(psutil.cpu_percent(interval=None), 1),
                "memory_percent": round(memory.percent, 1),
                "memory_used_bytes": int(memory.used),
                "memory_total_bytes": int(memory.total),
                "upload_bps": int(max(0.0, (net.bytes_sent - last_net.bytes_sent) / elapsed)),
                "download_bps": int(max(0.0, (net.bytes_recv - last_net.bytes_recv) / elapsed)),
                "sampled_at": time.time(),
                "hostname": socket.gethostname(),
            }
            with self._lock:
                self._stats = snapshot
            self._ready.set()
            last_sample_time = now
            last_net = net
            time.sleep(1)

    def get_stats(self):
        self.ensure_started()
        if not self._ready.is_set():
            self._ready.wait(timeout=0.25)
        with self._lock:
            stats = dict(self._stats)
        if stats["sampled_at"] is None:
            stats["sampled_at"] = time.time()
        return stats


def create_app(token=""):
    app = Flask(__name__)
    monitor = ResourceMonitor()
    expected_token = (token or "").strip()

    @app.route("/stats")
    def stats():
        if expected_token:
            supplied = (request.headers.get("X-Shiki-Token") or "").strip()
            if supplied != expected_token:
                return jsonify({"available": False, "error": "Unauthorized"}), 401
        return jsonify(monitor.get_stats())

    @app.route("/")
    def root():
        return jsonify({"ok": True, "endpoint": "/stats", "hostname": socket.gethostname()})

    return app


def main():
    parser = argparse.ArgumentParser(description="Expose local host resource statistics for Shiki Dashboard.")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address. Default: 0.0.0.0")
    parser.add_argument("--port", default=8765, type=int, help="Listen port. Default: 8765")
    parser.add_argument("--token", default=os.environ.get("SHIKI_HOST_TOKEN", ""), help="Optional shared token")
    args = parser.parse_args()

    if os.name == "nt":
        os.system("title ShikiDashboard Resource Monitor Agent")
    else:
        print("\33]0;ShikiDashboard Resource Monitor Agent\a", end="", flush=True)

    app = create_app(token=args.token)
    print(f"Remote host agent listening on http://{args.host}:{args.port}/stats")
    if args.token:
        print("Token protection enabled via X-Shiki-Token header")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
