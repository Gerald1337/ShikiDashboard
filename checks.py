import platform
import socket
import subprocess
import threading
import time
import requests as req_lib
from config import BROWSER_HEADERS, REACHABLE_CODES
from db import get_all_services, save_service_check, cleanup_old_service_checks
from smart import scan_all_drives

service_timers = {}


def check_service(service, use_local=False):
    if use_local:
        check_type = service.get("local_check_type", "tcp")
        url = service.get("local_url", "")
    else:
        check_type = service["check_type"]
        url = service["url"]

    if not url:
        return "unknown", 0, None, "No URL configured"

    start = time.time()
    try:
        if check_type in ("http", "https"):
            r = req_lib.get(url, timeout=120, allow_redirects=True, headers=BROWSER_HEADERS)
            ms = int((time.time() - start) * 1000)
            status = "up" if r.status_code in REACHABLE_CODES else "down"
            return status, ms, r.status_code, None
        elif check_type == "ping":
            host = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
            param = "-n" if platform.system().lower() == "windows" else "-c"
            result = subprocess.run(
                ["ping", param, "1", host],
                capture_output=True, text=True, timeout=120
            )
            ms = int((time.time() - start) * 1000)
            status = "up" if result.returncode == 0 else "down"
            return status, ms, None, None
        elif check_type == "tcp":
            host_port = url.replace("http://", "").replace("https://", "").split("/")[0]
            if ":" in host_port:
                host, port = host_port.rsplit(":", 1)
            else:
                host = host_port
                port = "80"
            sock = socket.create_connection((host, int(port)), timeout=120)
            sock.close()
            ms = int((time.time() - start) * 1000)
            return "up", ms, None, None
    except Exception as e:
        ms = int((time.time() - start) * 1000)
        return "down", ms, None, str(e)


def poll_service(service_id):
    services = get_all_services()
    svc = next((s for s in services if s["id"] == service_id), None)
    if not svc:
        return
    if svc.get("url"):
        try:
            status, ms, code, err = check_service(svc, use_local=False)
            save_service_check(service_id, status, ms, code, err, check_target='external')
        except Exception:
            pass
    if svc.get("local_url"):
        try:
            status, ms, code, err = check_service(svc, use_local=True)
            save_service_check(service_id, status, ms, code, err, check_target='local')
        except Exception:
            pass
    t = threading.Timer(svc["interval"], poll_service, args=[service_id])
    t.daemon = True
    service_timers[service_id] = t
    t.start()


def start_service_polling():
    services = get_all_services()
    for svc in services:
        t = threading.Timer(1, poll_service, args=[svc["id"]])
        t.daemon = True
        service_timers[svc["id"]] = t
        t.start()


def kick_service_poll(service_id):
    t = threading.Timer(5, poll_service, args=[service_id])
    t.daemon = True
    service_timers[service_id] = t
    t.start()


def background_drive_poll():
    while True:
        try:
            scan_all_drives()
        except Exception:
            pass
        time.sleep(3600)


def background_cleanup():
    while True:
        time.sleep(12 * 3600)
        try:
            cleanup_old_service_checks()
        except Exception as e:
            print(f"  [cleanup] Error: {e}")
