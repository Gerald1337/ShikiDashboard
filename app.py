from datetime import datetime
import json

from flask import Flask, jsonify, render_template_string, request
from db import (
    get_history,
    get_latest_snapshot_timestamp,
    get_latest_snapshots,
    get_nicknames,
    set_nickname,
    set_current_devices,
    get_all_services,
    add_service,
    update_service,
    delete_service,
    save_service_check,
    get_service_history,
    get_service_latest,
    get_service_uptime,
    save_service_order,
    get_drive_order,
    set_drive_order,
    get_app_setting,
    set_app_setting,
)
from smart import scan_all_drives
from checks import check_service, kick_service_poll, service_timers
from system_stats import get_system_stats
from templates import HTML

app = Flask(__name__)


def get_logo_config():
    raw = get_app_setting("app_logo")
    if not raw:
        return {"original_image": None, "crop": None}
    try:
        data = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {"original_image": None, "crop": None}
    return {
        "original_image": data.get("original_image"),
        "crop": data.get("crop"),
    }

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/app-logo")
def api_get_app_logo():
    return jsonify(get_logo_config())


@app.route("/api/app-logo", methods=["POST"])
def api_save_app_logo():
    data = request.get_json(silent=True) or {}
    original_image = data.get("original_image")
    crop = data.get("crop")

    if original_image is not None and not isinstance(original_image, str):
        return jsonify({"error": "original_image must be a string"}), 400
    if crop is not None and not isinstance(crop, dict):
        return jsonify({"error": "crop must be an object"}), 400

    if crop:
        try:
            crop = {
                "x": float(crop.get("x", 0)),
                "y": float(crop.get("y", 0)),
                "size": float(crop.get("size", 1)),
            }
        except (TypeError, ValueError):
            return jsonify({"error": "crop values must be numeric"}), 400

    set_app_setting("app_logo", json.dumps({
        "original_image": original_image,
        "crop": crop,
    }))
    return jsonify({"ok": True})


def apply_saved_drive_order(drives):
    order = get_drive_order()
    if not order:
        return drives
    by_device = {d.get("device"): d for d in drives}
    ordered = []
    for device in order:
        drive = by_device.pop(device, None)
        if drive:
            ordered.append(drive)
    for drive in drives:
        device = drive.get("device")
        if device in by_device:
            ordered.append(drive)
            by_device.pop(device, None)
    return ordered

@app.route("/api/drives")
def api_drives():
    drives = apply_saved_drive_order(scan_all_drives())
    set_current_devices([d["device"] for d in drives])
    timestamp = datetime.now().isoformat()
    for d in drives:
        d["timestamp"] = timestamp
    return jsonify(drives)

@app.route("/api/drives/summary")
def api_drives_summary():
    drives = scan_all_drives()
    temps = [d["temperature"] for d in drives if d.get("temperature") is not None]
    last_scanned = datetime.now().isoformat()
    return jsonify({
        "total": len(drives),
        "healthy": sum(1 for d in drives if d.get("health") == "PASS"),
        "failing": sum(1 for d in drives if d.get("health") == "FAIL"),
        "avg_temp": round(sum(temps) / len(temps)) if temps else None,
        "max_temp": max(temps) if temps else None,
        "last_scanned": last_scanned,
    })

@app.route("/api/drives/cached")
def api_drives_cached():
    return jsonify(apply_saved_drive_order(get_latest_snapshots()))

@app.route("/api/drives/order", methods=["POST"])
def api_set_drive_order():
    data = request.get_json() or {}
    order = data.get("order")
    if not isinstance(order, list):
        return jsonify({"error": "order must be a list"}), 400
    set_drive_order(order)
    return jsonify({"ok": True})

@app.route("/api/drives/summary/cached")
def api_drives_summary_cached():
    drives = get_latest_snapshots()
    temps = [d["temperature"] for d in drives if d.get("temperature") is not None]
    return jsonify({
        "total": len(drives),
        "healthy": sum(1 for d in drives if d.get("health") == "PASS"),
        "failing": sum(1 for d in drives if d.get("health") == "FAIL"),
        "avg_temp": round(sum(temps) / len(temps)) if temps else None,
        "max_temp": max(temps) if temps else None,
        "last_scanned": get_latest_snapshot_timestamp(),
    })

@app.route("/api/system-stats")
def api_system_stats():
    return jsonify(get_system_stats())

@app.route("/api/history/<path:device>")
def api_history(device):
    device = "/" + device if not device.startswith("/") else device
    return jsonify(get_history(device))

@app.route("/api/nicknames")
def api_get_nicknames():
    return jsonify(get_nicknames())

@app.route("/api/nickname", methods=["POST"])
def api_set_nickname():
    data = request.get_json()
    device = data.get("device", "")
    nickname = data.get("nickname", "")
    if not device:
        return jsonify({"error": "device required"}), 400
    set_nickname(device, nickname)
    return jsonify({"ok": True})

@app.route("/api/services")
def api_get_services():
    services = get_all_services()
    result = []
    for svc in services:
        has_external = bool(svc.get("url"))
        latest_ext = get_service_latest(svc["id"], check_target='external')
        latest_local = get_service_latest(svc["id"], check_target='local') if svc.get("local_url") else None
        uptime_ext = get_service_uptime(svc["id"], check_target='external')
        uptime_local = get_service_uptime(svc["id"], check_target='local') if svc.get("local_url") else None
        recent_ext = get_service_history(svc["id"], limit=30, check_target='external')
        recent_local = get_service_history(svc["id"], limit=30, check_target='local') if svc.get("local_url") else []
        result.append({
            **svc,
            "latest": latest_ext if has_external else latest_local,
            "latest_local": latest_local,
            "uptime": uptime_ext if has_external else uptime_local,
            "uptime_local": uptime_local,
            "recent_history": recent_ext if has_external else recent_local,
            "recent_history_local": recent_local,
        })
    return jsonify(result)

@app.route("/api/services/summary")
def api_services_summary():
    services = get_all_services()
    total = len(services)
    up = 0
    down = 0
    for svc in services:
        if svc.get("url"):
            latest = get_service_latest(svc["id"], check_target='external')
        else:
            latest = get_service_latest(svc["id"], check_target='local')
        if latest:
            if latest["status"] == "up":
                up += 1
            else:
                down += 1
    return jsonify({"total": total, "up": up, "down": down, "unknown": total - up - down})

@app.route("/api/services", methods=["POST"])
def api_add_service():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    url = (data.get("url") or "").strip()
    check_type = data.get("check_type", "http")
    interval = int(data.get("interval", 60))
    chart_window_sec = int(data.get("chart_window_sec", 2700))
    local_url = (data.get("local_url") or "").strip()
    local_check_type = data.get("local_check_type", "tcp")
    if not name or not local_url:
        return jsonify({"error": "name and local_url required"}), 400
    service_id = add_service(name, url or "", check_type, interval, chart_window_sec, local_url, local_check_type)
    kick_service_poll(service_id)
    return jsonify({"ok": True, "id": service_id})

@app.route("/api/services/<int:service_id>", methods=["PATCH"])
def api_update_service(service_id):
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    url = (data.get("url") or "").strip()
    check_type = data.get("check_type", "http")
    interval = int(data.get("interval", 60))
    chart_window_sec = int(data.get("chart_window_sec", 2700))
    local_url = (data.get("local_url") or "").strip()
    local_check_type = data.get("local_check_type", "tcp")
    if not name or not local_url:
        return jsonify({"error": "name and local_url required"}), 400
    update_service(service_id, name, url or "", check_type, interval, chart_window_sec, local_url, local_check_type)
    if service_id in service_timers:
        service_timers[service_id].cancel()
    kick_service_poll(service_id)
    return jsonify({"ok": True})

@app.route("/api/services/<int:service_id>", methods=["DELETE"])
def api_delete_service(service_id):
    if service_id in service_timers:
        service_timers[service_id].cancel()
        del service_timers[service_id]
    delete_service(service_id)
    return jsonify({"ok": True})

@app.route("/api/services/order", methods=["POST"])
def api_save_service_order():
    data = request.get_json() or {}
    order = data.get("order")
    if not isinstance(order, list):
        return jsonify({"error": "order must be a list of service IDs"}), 400
    save_service_order(order)
    return jsonify({"ok": True})

@app.route("/api/services/<int:service_id>/history")
def api_service_history(service_id):
    target = request.args.get("target", "external")
    return jsonify(get_service_history(service_id, check_target=target))

@app.route("/api/services/<int:service_id>/check", methods=["POST"])
def api_service_check_now(service_id):
    services = get_all_services()
    svc = next((s for s in services if s["id"] == service_id), None)
    if not svc:
        return jsonify({"error": "not found"}), 404
    result = {}
    if svc.get("url"):
        status, ms, code, err = check_service(svc, use_local=False)
        save_service_check(service_id, status, ms, code, err, check_target='external')
        result["external"] = {"status": status, "response_ms": ms, "status_code": code, "error": err}
    if svc.get("local_url"):
        lstatus, lms, lcode, lerr = check_service(svc, use_local=True)
        save_service_check(service_id, lstatus, lms, lcode, lerr, check_target='local')
        result["local"] = {"status": lstatus, "response_ms": lms, "status_code": lcode, "error": lerr}
    return jsonify(result)
