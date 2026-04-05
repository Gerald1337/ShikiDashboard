from datetime import datetime
import json
from urllib.parse import urlencode, urlsplit, urlunsplit

from flask import Flask, jsonify, render_template_string, request
import requests as req_lib
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
    get_debrid_config,
    set_debrid_config,
    get_all_hosts,
    add_host,
    update_host,
    delete_host,
    save_host_order,
    get_host_history,
)
from smart import scan_all_drives
from checks import check_service, kick_service_poll, service_timers
from host_monitor import (
    HOST_STATS_WINDOW_SEC,
    LOCAL_HOST_ID,
    get_all_host_history,
    get_hosts_with_latest,
    kick_host_poll,
    stop_host_poll,
)
from routes import register_screen_routes
from system_stats import get_system_stats
from templates import HTML
from widgets import (
    OVERVIEW_WIDGET_STYLES,
    OVERVIEW_WIDGET_TYPE_METADATA,
    render_overview_widgets,
    sanitize_overview_widget_layout,
)

app = Flask(__name__)
TAB_SECTIONS = {"overview", "services", "hosts", "disks", "debrid"}
EMBY_RECENT_LIMIT = 6


def parse_int(value, default, minimum=None, maximum=None):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    if minimum is not None:
        parsed = max(minimum, parsed)
    if maximum is not None:
        parsed = min(maximum, parsed)
    return parsed


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


def get_debrid_connection_details():
    config = get_debrid_config() or {}
    ip = (config.get("ip") or "").strip()
    username = (config.get("username") or "").strip()
    password = (config.get("password") or "") or ""
    return ip, username, password


def make_debrid_proxy_response(resp):
    body = resp.text or ""
    json_body = None
    try:
        json_body = resp.json()
    except ValueError:
        json_body = None
    return jsonify({
        "status_code": resp.status_code,
        "ok": resp.ok,
        "body": body,
        "json": json_body,
        "content_type": resp.headers.get("Content-Type", ""),
    }), resp.status_code if resp.status_code >= 400 else 200


def proxy_debrid_post(endpoint_path, payload, failure_message):
    ip, username, password = get_debrid_connection_details()
    if not ip or not username:
        return jsonify({"error": "Debrid client is not configured"}), 400
    url = f"http://{ip}{endpoint_path}"
    try:
        resp = req_lib.post(
            url,
            auth=(username, password),
            json=payload,
            timeout=10,
        )
    except req_lib.RequestException as exc:
        return jsonify({"error": failure_message, "detail": str(exc)}), 502
    return make_debrid_proxy_response(resp)


def normalize_emby_host(raw_host):
    host = (raw_host or "").strip()
    if not host:
        return ""
    if "://" not in host:
        host = f"http://{host}"
    parsed = urlsplit(host)
    path = (parsed.path or "").rstrip("/")
    if not path:
        path = "/emby"
    normalized = parsed._replace(path=path, query="", fragment="")
    return urlunsplit(normalized).rstrip("/")


def make_emby_headers(token):
    return {"X-Emby-Token": token}


def fetch_emby_json(host, token, path, *, params=None, timeout=10):
    url = f"{host}{path}"
    resp = req_lib.get(url, headers=make_emby_headers(token), params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def ping_emby_server(host, token, timeout=5):
    url = f"{host}/System/Ping"
    resp = req_lib.get(url, headers=make_emby_headers(token), timeout=timeout)
    resp.raise_for_status()
    return {
        "ok": True,
        "status_code": resp.status_code,
    }


def build_emby_image_url(host, token, item_id, *, item_type="Items", max_height=None, max_width=None):
    normalized_id = str(item_id or "").strip()
    if not normalized_id:
        return None
    query = {"api_key": token}
    if max_height:
        query["MaxHeight"] = int(max_height)
    if max_width:
        query["MaxWidth"] = int(max_width)
    return f"{host}/{item_type}/{normalized_id}/Images/Primary?{urlencode(query)}"


def normalize_emby_user(item):
    if not isinstance(item, dict):
        return None
    user_id = str(item.get("Id") or item.get("id") or "").strip()
    if not user_id:
        return None
    return {
        "id": user_id,
        "name": (item.get("Name") or item.get("name") or "").strip() or "Unnamed user",
    }


def fetch_emby_users(host, token):
    user_sources = []
    for path in ("/Users/Query", "/Users/Public"):
        try:
            payload = fetch_emby_json(host, token, path)
        except req_lib.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else None
            if status_code in {401, 403, 404}:
                continue
            raise
        items = payload.get("Items") if isinstance(payload, dict) else payload
        users = []
        for item in items or []:
            normalized = normalize_emby_user(item)
            if normalized:
                users.append(normalized)
        if users:
            user_sources = users
            break
    return user_sources


def choose_emby_user(host, token, requested_user_id=None):
    users = fetch_emby_users(host, token)
    resolved = None
    if requested_user_id:
        resolved = next((user for user in users if user["id"] == str(requested_user_id).strip()), None)
        if resolved is None:
            requested = str(requested_user_id).strip()
            if requested:
                resolved = {"id": requested, "name": "Selected user"}
    if resolved is None and users:
        resolved = users[0]
    return resolved, users


def normalize_emby_session(session):
    if not isinstance(session, dict) or not isinstance(session.get("NowPlayingItem"), dict):
        return None
    item = session.get("NowPlayingItem") or {}
    play_state = session.get("PlayState") or {}
    runtime_ticks = item.get("RunTimeTicks")
    position_ticks = play_state.get("PositionTicks")
    progress_percent = None
    try:
        runtime_ticks = int(runtime_ticks)
        position_ticks = int(position_ticks)
        if runtime_ticks > 0 and position_ticks >= 0:
            progress_percent = max(0.0, min(100.0, (position_ticks / runtime_ticks) * 100))
    except (TypeError, ValueError, ZeroDivisionError):
        progress_percent = None
    return {
        "user_id": str(session.get("UserId") or "").strip(),
        "user_name": (session.get("UserName") or "").strip() or "Unknown user",
        "device_name": (session.get("DeviceName") or "").strip() or (session.get("Client") or "").strip() or "Unknown device",
        "client": (session.get("Client") or "").strip(),
        "is_paused": bool(play_state.get("IsPaused")),
        "progress_percent": round(progress_percent, 1) if progress_percent is not None else None,
        "item": {
            "id": str(item.get("Id") or "").strip(),
            "name": (item.get("Name") or "").strip() or "Untitled",
            "series_name": (item.get("SeriesName") or "").strip(),
            "type": (item.get("Type") or "").strip(),
            "production_year": item.get("ProductionYear"),
            "index_number": item.get("IndexNumber"),
            "parent_index_number": item.get("ParentIndexNumber"),
            "series_id": str(item.get("SeriesId") or "").strip(),
        },
    }


def normalize_emby_latest_item(item):
    if not isinstance(item, dict):
        return None
    item_id = str(item.get("Id") or "").strip()
    if not item_id:
        return None
    return {
        "id": item_id,
        "name": (item.get("Name") or "").strip() or "Untitled",
        "series_name": (item.get("SeriesName") or "").strip(),
        "series_id": str(item.get("SeriesId") or "").strip(),
        "type": (item.get("Type") or "").strip(),
        "date_created": item.get("DateCreated"),
        "production_year": item.get("ProductionYear"),
        "index_number": item.get("IndexNumber"),
        "parent_index_number": item.get("ParentIndexNumber"),
    }


def group_emby_recent_items(items, limit):
    grouped = []
    seen = set()
    for item in items:
        item_type = (item.get("type") or "").lower()
        if item_type == "episode":
            group_id = item.get("series_id") or item.get("id")
            display_name = item.get("series_name") or item.get("name") or "Untitled"
            grouped_type = "Series"
            image_item_id = item.get("series_id") or item.get("id")
        else:
            group_id = item.get("id")
            display_name = item.get("name") or "Untitled"
            grouped_type = item.get("type") or "Item"
            image_item_id = item.get("id")
        if not group_id or group_id in seen:
            continue
        grouped.append({
            **item,
            "name": display_name,
            "type": grouped_type,
            "image_item_id": image_item_id,
        })
        seen.add(group_id)
        if len(grouped) >= limit:
            break
    return grouped


def build_emby_widget_payload(host, token, user_id=None):
    normalized_host = normalize_emby_host(host)
    normalized_token = (token or "").strip()
    if not normalized_host or not normalized_token:
        raise ValueError("Emby host and token are required")

    resolved_user, users = choose_emby_user(normalized_host, normalized_token, user_id)
    if resolved_user is None:
        raise ValueError("No Emby users were found for this server")

    sessions_payload = fetch_emby_json(normalized_host, normalized_token, "/Sessions")
    latest_payload = fetch_emby_json(
        normalized_host,
        normalized_token,
        f"/Users/{resolved_user['id']}/Items",
        params={
            "Recursive": "true",
            "IncludeItemTypes": "Movie,Episode",
            "SortBy": "DateCreated",
            "SortOrder": "Descending",
            "Limit": max(EMBY_RECENT_LIMIT * 10, 50),
            "Fields": "DateCreated",
        },
    )

    sessions = []
    for item in sessions_payload or []:
        normalized = normalize_emby_session(item)
        if normalized:
            sessions.append(normalized)

    latest_items = []
    latest_payload_items = latest_payload.get("Items") if isinstance(latest_payload, dict) else latest_payload
    for item in latest_payload_items or []:
        normalized = normalize_emby_latest_item(item)
        if normalized:
            latest_items.append(normalized)

    grouped_recent_items = group_emby_recent_items(latest_items, EMBY_RECENT_LIMIT)

    for session in sessions:
        session["user_image_url"] = build_emby_image_url(
            normalized_host,
            normalized_token,
            session.get("user_id"),
            item_type="Users",
            max_height=48,
            max_width=48,
        )

    for item in grouped_recent_items:
        item["image_url"] = build_emby_image_url(
            normalized_host,
            normalized_token,
            item.get("image_item_id") or item.get("id"),
            item_type="Items",
            max_height=180,
            max_width=120,
        )

    return {
        "host": normalized_host,
        "resolved_user_id": resolved_user["id"],
        "resolved_user_name": resolved_user["name"],
        "users": users,
        "active_sessions": sessions,
        "recent_items": grouped_recent_items[:EMBY_RECENT_LIMIT],
        "updated_at": datetime.now().isoformat(),
    }

def get_saved_overview_widget_layout():
    raw = get_app_setting("overview_panel_order")
    parsed = None
    if raw:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = None
    layout = sanitize_overview_widget_layout(parsed)
    normalized_layout_json = json.dumps(layout)
    if raw != normalized_layout_json:
        set_app_setting("overview_panel_order", normalized_layout_json)
    return layout


def render_dashboard(initial_section="overview"):
    if initial_section not in TAB_SECTIONS:
        initial_section = "overview"
    overview_widget_layout = get_saved_overview_widget_layout()
    return render_template_string(
        HTML,
        initial_section=initial_section,
        overview_widget_styles=OVERVIEW_WIDGET_STYLES,
        overview_widgets=render_overview_widgets(overview_widget_layout),
        overview_widget_layout_json=json.dumps(overview_widget_layout),
        overview_widget_type_metadata_json=json.dumps(OVERVIEW_WIDGET_TYPE_METADATA),
    )


register_screen_routes(app, render_dashboard)


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


@app.route("/api/debrid-config")
def api_get_debrid_config():
    return jsonify(get_debrid_config() or {})


@app.route("/api/debrid-config", methods=["POST"])
def api_save_debrid_config():
    data = request.get_json(silent=True) or {}
    ip = (data.get("ip") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    set_debrid_config(ip, username, password)
    return jsonify({"ok": True})


@app.route("/api/debrid-queue")
def api_rdt_client_queue():
    ip, username, password = get_debrid_connection_details()
    if not ip or not username:
        return jsonify({"error": "Debrid client is not configured"}), 400
    url = f"http://{ip}/Api/ShikiDashboard/Queue/Public"
    try:
        resp = req_lib.get(url, auth=(username, password), timeout=10)
    except req_lib.RequestException as exc:
        return jsonify({"error": "Failed to fetch Debrid queue", "detail": str(exc)}), 502
    return make_debrid_proxy_response(resp)


@app.route("/api/debrid-ingest-magnet", methods=["POST"])
def api_debrid_ingest_magnet():
    data = request.get_json(silent=True) or {}
    magnet_link = (data.get("magnetLink") or "").strip()
    if not magnet_link:
        return jsonify({"error": "magnetLink is required"}), 400
    if not magnet_link.lower().startswith("magnet:?"):
        return jsonify({"error": "magnetLink must start with magnet:?"}), 400
    return proxy_debrid_post(
        "/Api/ShikiDashboard/IngestMagnetLink",
        {"magnetLink": magnet_link},
        "Failed to forward magnet link",
    )


@app.route("/api/debrid-edit-queue/remove", methods=["POST"])
def api_debrid_edit_queue_remove():
    data = request.get_json(silent=True) or {}
    torrent_id = data.get("torrentId")
    if torrent_id is None or str(torrent_id).strip() == "":
        return jsonify({"error": "torrentId is required"}), 400
    return proxy_debrid_post(
        "/Api/ShikiDashboard/EditQueue/Remove",
        {"torrentId": torrent_id},
        "Failed to remove torrent from queue",
    )


@app.route("/api/debrid-edit-queue/retry", methods=["POST"])
def api_debrid_edit_queue_retry():
    data = request.get_json(silent=True) or {}
    torrent_id = data.get("torrentId")
    if torrent_id is None or str(torrent_id).strip() == "":
        return jsonify({"error": "torrentId is required"}), 400
    return proxy_debrid_post(
        "/Api/ShikiDashboard/EditQueue/Retry",
        {"torrentId": torrent_id},
        "Failed to retry torrent in queue",
    )


@app.route("/api/emby/users", methods=["POST"])
def api_emby_users():
    data = request.get_json(silent=True) or {}
    host = data.get("host")
    token = data.get("token")
    normalized_host = normalize_emby_host(host)
    normalized_token = (token or "").strip()
    if not normalized_host or not normalized_token:
        return jsonify({"error": "host and token are required"}), 400
    try:
        users = fetch_emby_users(normalized_host, normalized_token)
    except req_lib.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 502
        detail = exc.response.text.strip() if exc.response is not None else str(exc)
        return jsonify({"error": "Failed to load Emby users", "detail": detail or str(exc)}), status_code
    except req_lib.RequestException as exc:
        return jsonify({"error": "Failed to load Emby users", "detail": str(exc)}), 502
    return jsonify({
        "host": normalized_host,
        "users": users,
    })


@app.route("/api/emby/widget-data", methods=["POST"])
def api_emby_widget_data():
    data = request.get_json(silent=True) or {}
    host = data.get("host")
    token = data.get("token")
    user_id = data.get("user_id")
    try:
        payload = build_emby_widget_payload(host, token, user_id=user_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except req_lib.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 502
        detail = exc.response.text.strip() if exc.response is not None else str(exc)
        return jsonify({"error": "Failed to fetch Emby data", "detail": detail or str(exc)}), status_code
    except req_lib.RequestException as exc:
        return jsonify({"error": "Failed to fetch Emby data", "detail": str(exc)}), 502
    return jsonify(payload)


@app.route("/api/emby/ping", methods=["POST"])
def api_emby_ping():
    data = request.get_json(silent=True) or {}
    host = normalize_emby_host(data.get("host"))
    token = (data.get("token") or "").strip()
    if not host or not token:
        return jsonify({"error": "host and token are required"}), 400
    try:
        payload = ping_emby_server(host, token)
    except req_lib.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 502
        detail = exc.response.text.strip() if exc.response is not None else str(exc)
        return jsonify({
            "ok": False,
            "host": host,
            "status_code": status_code,
            "detail": detail or str(exc),
        }), status_code
    except req_lib.RequestException as exc:
        return jsonify({
            "ok": False,
            "host": host,
            "detail": str(exc),
        }), 502
    return jsonify({
        "host": host,
        **payload,
    })


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


@app.route("/api/overview/order")
def api_get_overview_order():
    layout = get_saved_overview_widget_layout()
    return jsonify({
        "layout": layout,
        "order": [widget["instance_id"] for widget in layout],
        "widgets_html": render_overview_widgets(layout),
    })


@app.route("/api/overview/order", methods=["POST"])
def api_save_overview_order():
    data = request.get_json() or {}
    layout = sanitize_overview_widget_layout(data.get("layout", data.get("order")))
    set_app_setting("overview_panel_order", json.dumps(layout))
    return jsonify({
        "ok": True,
        "layout": layout,
        "order": [widget["instance_id"] for widget in layout],
        "widgets_html": render_overview_widgets(layout),
    })

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


@app.route("/api/hosts")
def api_get_hosts():
    return jsonify(get_hosts_with_latest())


@app.route("/api/hosts/history")
def api_get_hosts_history():
    window_sec = parse_int(request.args.get("window", HOST_STATS_WINDOW_SEC), HOST_STATS_WINDOW_SEC, minimum=10, maximum=3600)
    return jsonify(get_all_host_history(window_sec=window_sec))


@app.route("/api/hosts/<int:host_id>/history")
def api_get_host_history(host_id):
    window_sec = parse_int(request.args.get("window", HOST_STATS_WINDOW_SEC), HOST_STATS_WINDOW_SEC, minimum=10, maximum=3600)
    return jsonify(get_host_history(host_id, window_sec=window_sec))


@app.route("/api/hosts", methods=["POST"])
def api_add_host():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    host = (data.get("host") or "").strip()
    token = (data.get("token") or "").strip()
    port = parse_int(data.get("port", 8765), 8765, minimum=1, maximum=65535)
    interval = parse_int(data.get("interval", 1), 1, minimum=1, maximum=60)
    if not name or not host:
        return jsonify({"error": "name and host required"}), 400
    host_id = add_host(name, host, port, token, interval)
    kick_host_poll(host_id)
    return jsonify({"ok": True, "id": host_id})


@app.route("/api/hosts/<int:host_id>", methods=["PATCH"])
def api_update_host(host_id):
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if host_id == LOCAL_HOST_ID:
        if not name:
            return jsonify({"error": "name required"}), 400
        set_app_setting("local_host_name", name)
        kick_host_poll(host_id, delay=0.01)
        return jsonify({"ok": True})
    host = (data.get("host") or "").strip()
    token = (data.get("token") or "").strip()
    port = parse_int(data.get("port", 8765), 8765, minimum=1, maximum=65535)
    interval = parse_int(data.get("interval", 1), 1, minimum=1, maximum=60)
    if not name or not host:
        return jsonify({"error": "name and host required"}), 400
    update_host(host_id, name, host, port, token, interval)
    kick_host_poll(host_id)
    return jsonify({"ok": True})


@app.route("/api/hosts/<int:host_id>", methods=["DELETE"])
def api_delete_host(host_id):
    if host_id == LOCAL_HOST_ID:
        return jsonify({"error": "local host is built in"}), 400
    stop_host_poll(host_id)
    delete_host(host_id)
    return jsonify({"ok": True})


@app.route("/api/hosts/order", methods=["POST"])
def api_save_host_order():
    data = request.get_json(silent=True) or {}
    order = data.get("order")
    if not isinstance(order, list):
        return jsonify({"error": "order must be a list of host IDs"}), 400
    normalized_order = []
    for host_id in order:
        parsed = parse_int(host_id, -1)
        if parsed >= 0:
            normalized_order.append(parsed)
    save_host_order(normalized_order)
    return jsonify({"ok": True})


@app.route("/api/hosts/<int:host_id>/check", methods=["POST"])
def api_host_check_now(host_id):
    if host_id != LOCAL_HOST_ID:
        host = next((item for item in get_all_hosts() if item["id"] == host_id), None)
        if not host:
            return jsonify({"error": "not found"}), 404
    else:
        host = {"id": LOCAL_HOST_ID}
    if not host:
        return jsonify({"error": "not found"}), 404
    kick_host_poll(host_id, delay=0.01)
    return jsonify({"ok": True})

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
