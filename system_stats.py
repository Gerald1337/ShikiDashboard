import threading
import time

try:
    import psutil
except ImportError:  # pragma: no cover - handled at runtime based on environment
    psutil = None


class SystemStatsMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self._started = False
        self._thread = None
        self._ready = threading.Event()
        self._stats = self._empty_stats()

    def _empty_stats(self):
        return {
            "available": psutil is not None,
            "error": None if psutil is not None else "psutil is not installed",
            "cpu_percent": None,
            "memory_percent": None,
            "memory_used_bytes": None,
            "memory_total_bytes": None,
            "upload_bps": None,
            "download_bps": None,
            "sampled_at": None,
        }

    def ensure_started(self):
        if self._started or psutil is None:
            return
        with self._lock:
            if self._started:
                return
            self._started = True
            self._thread = threading.Thread(target=self._run, daemon=True, name="system-stats-monitor")
            self._thread.start()

    def _run(self):
        psutil.cpu_percent(interval=None)
        last_sample_time = time.time()
        last_net = psutil.net_io_counters()

        while True:
            now = time.time()
            mem = psutil.virtual_memory()
            net = psutil.net_io_counters()
            elapsed = max(now - last_sample_time, 0.001)

            upload_bps = max(0.0, (net.bytes_sent - last_net.bytes_sent) / elapsed)
            download_bps = max(0.0, (net.bytes_recv - last_net.bytes_recv) / elapsed)

            snapshot = {
                "available": True,
                "error": None,
                "cpu_percent": round(psutil.cpu_percent(interval=None), 1),
                "memory_percent": round(mem.percent, 1),
                "memory_used_bytes": int(mem.used),
                "memory_total_bytes": int(mem.total),
                "upload_bps": int(upload_bps),
                "download_bps": int(download_bps),
                "sampled_at": time.time(),
            }
            with self._lock:
                self._stats = snapshot
            self._ready.set()

            last_sample_time = now
            last_net = net
            time.sleep(1)

    def get_stats(self):
        self.ensure_started()
        if psutil is not None and not self._ready.is_set():
            self._ready.wait(timeout=0.25)
        with self._lock:
            stats = dict(self._stats)
        if stats["sampled_at"] is None:
            stats["sampled_at"] = time.time()
        return stats


monitor = SystemStatsMonitor()


def get_system_stats():
    return monitor.get_stats()
