from datetime import datetime
import json
import socket
import threading
import time

import requests as req_lib

from config import BROWSER_HEADERS
from db import (
    cleanup_old_host_samples,
    get_all_hosts,
    get_app_setting,
    get_host_history,
    get_host_latest_sample,
    save_host_sample,
)
from system_stats import get_system_stats


HOST_STATS_WINDOW_SEC = 60
LOCAL_HOST_ID = 0
LOCAL_HOST_INTERVAL = 1
host_timers = {}
HOST_SAMPLE_CLEANUP_INTERVAL_SEC = 300
_last_host_sample_cleanup = 0.0


def get_local_host_definition():
    hostname = socket.gethostname()
    display_name = (get_app_setting("local_host_name", hostname) or "").strip() or hostname
    return {
        "id": LOCAL_HOST_ID,
        "name": display_name,
        "host": "localhost",
        "port": 8080,
        "token": "",
        "interval": LOCAL_HOST_INTERVAL,
        "created_at": None,
        "is_local": True,
    }


def get_ordered_host_definitions():
    local_host = get_local_host_definition()
    remote_hosts = get_all_hosts()
    default_hosts = [local_host, *remote_hosts]
    host_map = {host["id"]: host for host in default_hosts}

    raw_order = get_app_setting("host_order", "[]")
    try:
        saved_order = json.loads(raw_order) if raw_order else []
    except (TypeError, ValueError, json.JSONDecodeError):
        saved_order = []

    ordered_hosts = []
    seen = set()
    for host_id in saved_order:
        if not isinstance(host_id, int) or host_id in seen:
            continue
        host = host_map.get(host_id)
        if not host:
            continue
        ordered_hosts.append(host)
        seen.add(host_id)

    ordered_hosts.extend(host for host in default_hosts if host["id"] not in seen)
    return ordered_hosts


def build_host_url(host):
    return f"http://{host['host']}:{host['port']}/stats"


def normalize_remote_stats(data):
    if not isinstance(data, dict):
        return {"available": False, "error": "Invalid response payload"}
    return {
        "available": bool(data.get("available", True)),
        "error": data.get("error"),
        "cpu_percent": data.get("cpu_percent"),
        "memory_percent": data.get("memory_percent"),
        "memory_used_bytes": data.get("memory_used_bytes"),
        "memory_total_bytes": data.get("memory_total_bytes"),
        "upload_bps": data.get("upload_bps"),
        "download_bps": data.get("download_bps"),
        "sampled_at": data.get("sampled_at"),
        "hostname": data.get("hostname"),
    }


def fetch_host_stats(host):
    headers = {"Accept": "application/json", **BROWSER_HEADERS}
    if host.get("token"):
        headers["X-Shiki-Token"] = host["token"]
    response = req_lib.get(
        build_host_url(host),
        headers=headers,
        timeout=max(2, min(int(host.get("interval") or 3), 10)),
    )
    response.raise_for_status()
    return normalize_remote_stats(response.json())


def poll_local_host():
    try:
        stats = get_system_stats()
        reachable = bool(stats.get("available"))
        error = stats.get("error") if not reachable else None
        save_host_sample(LOCAL_HOST_ID, reachable=reachable, error=error, stats=stats)
    except Exception as exc:
        save_host_sample(LOCAL_HOST_ID, reachable=False, error=str(exc), stats={})
    _maybe_cleanup_host_samples()

    timer = threading.Timer(LOCAL_HOST_INTERVAL, poll_local_host)
    timer.daemon = True
    host_timers[LOCAL_HOST_ID] = timer
    timer.start()


def poll_host(host_id):
    hosts = get_all_hosts()
    host = next((item for item in hosts if item["id"] == host_id), None)
    if not host:
        return

    try:
        stats = fetch_host_stats(host)
        reachable = bool(stats.get("available"))
        error = stats.get("error") if not reachable else None
        save_host_sample(host_id, reachable=reachable, error=error, stats=stats)
    except Exception as exc:
        save_host_sample(host_id, reachable=False, error=str(exc), stats={})
    _maybe_cleanup_host_samples()

    timer = threading.Timer(host["interval"], poll_host, args=[host_id])
    timer.daemon = True
    host_timers[host_id] = timer
    timer.start()


def start_host_polling():
    local_timer = threading.Timer(1, poll_local_host)
    local_timer.daemon = True
    host_timers[LOCAL_HOST_ID] = local_timer
    local_timer.start()
    for host in get_all_hosts():
        timer = threading.Timer(1, poll_host, args=[host["id"]])
        timer.daemon = True
        host_timers[host["id"]] = timer
        timer.start()


def kick_host_poll(host_id, delay=0.25):
    if host_id == LOCAL_HOST_ID:
        if host_id in host_timers:
            host_timers[host_id].cancel()
        timer = threading.Timer(delay, poll_local_host)
        timer.daemon = True
        host_timers[host_id] = timer
        timer.start()
        return
    if host_id in host_timers:
        host_timers[host_id].cancel()
    timer = threading.Timer(delay, poll_host, args=[host_id])
    timer.daemon = True
    host_timers[host_id] = timer
    timer.start()


def stop_host_poll(host_id):
    if host_id in host_timers:
        host_timers[host_id].cancel()
        del host_timers[host_id]


def get_hosts_with_latest():
    hosts = []
    now = datetime.now()
    for host in get_ordered_host_definitions():
        latest = get_host_latest_sample(host["id"])
        status = "unknown"
        if latest:
            age = max((now - datetime.fromisoformat(latest["timestamp"])).total_seconds(), 0)
            if latest["reachable"]:
                status = "stale" if age > max(host["interval"] * 3, 10) else "live"
            else:
                status = "offline"
        hosts.append({
            **host,
            "url": "Built in" if host.get("is_local") else build_host_url(host),
            "latest": latest,
            "status": status,
        })
    return hosts


def get_all_host_history(window_sec=HOST_STATS_WINDOW_SEC):
    hosts = get_ordered_host_definitions()
    return {
        str(host["id"]): get_host_history(host["id"], window_sec=window_sec)
        for host in hosts
    }


def prune_host_history():
    _maybe_cleanup_host_samples(force=True)


def _maybe_cleanup_host_samples(force=False):
    global _last_host_sample_cleanup
    now = time.monotonic()
    if not force and now - _last_host_sample_cleanup < HOST_SAMPLE_CLEANUP_INTERVAL_SEC:
        return
    _last_host_sample_cleanup = now
    try:
        cleanup_old_host_samples()
    except Exception:
        pass
