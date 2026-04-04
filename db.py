import sqlite3
import json
from datetime import datetime, timedelta
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            device TEXT NOT NULL,
            temperature INTEGER,
            health TEXT,
            data TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS nicknames (
            device TEXT PRIMARY KEY,
            nickname TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            check_type TEXT NOT NULL DEFAULT 'http',
            interval INTEGER NOT NULL DEFAULT 60,
            chart_window_sec INTEGER NOT NULL DEFAULT 2700,
            local_url TEXT,
            local_check_type TEXT NOT NULL DEFAULT 'tcp',
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS service_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            response_ms INTEGER,
            status_code INTEGER,
            error TEXT,
            check_target TEXT NOT NULL DEFAULT 'external',
            FOREIGN KEY(service_id) REFERENCES services(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS current_devices (
            device TEXT PRIMARY KEY
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS drive_order (
            device TEXT PRIMARY KEY,
            sort_order INTEGER NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS debrid_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            ip TEXT,
            username TEXT,
            password TEXT,
            updated_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host TEXT NOT NULL,
            port INTEGER NOT NULL DEFAULT 8765,
            token TEXT,
            interval INTEGER NOT NULL DEFAULT 3,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS host_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            reachable INTEGER NOT NULL DEFAULT 0,
            error TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            memory_used_bytes INTEGER,
            memory_total_bytes INTEGER,
            upload_bps INTEGER,
            download_bps INTEGER,
            sampled_at REAL,
            FOREIGN KEY(host_id) REFERENCES hosts(id)
        )
    """)
    conn.commit()
    conn.close()


def migrate_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA table_info(services)")
    svc_cols = [row[1] for row in c.fetchall()]
    if 'chart_window_sec' not in svc_cols:
        c.execute("ALTER TABLE services ADD COLUMN chart_window_sec INTEGER NOT NULL DEFAULT 2700")
    else:
        c.execute("UPDATE services SET chart_window_sec = 2700 WHERE chart_window_sec = 600 OR chart_window_sec IS NULL")
    if 'local_url' not in svc_cols:
        c.execute("ALTER TABLE services ADD COLUMN local_url TEXT")
    if 'local_check_type' not in svc_cols:
        c.execute("ALTER TABLE services ADD COLUMN local_check_type TEXT NOT NULL DEFAULT 'tcp'")
    if 'sort_order' not in svc_cols:
        c.execute("ALTER TABLE services ADD COLUMN sort_order INTEGER NOT NULL DEFAULT 0")
        c.execute("UPDATE services SET sort_order = id")

    c.execute("PRAGMA table_info(service_checks)")
    chk_cols = [row[1] for row in c.fetchall()]
    if 'check_target' not in chk_cols:
        c.execute("ALTER TABLE service_checks ADD COLUMN check_target TEXT NOT NULL DEFAULT 'external'")

    c.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS debrid_config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            ip TEXT,
            username TEXT,
            password TEXT,
            updated_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host TEXT NOT NULL,
            port INTEGER NOT NULL DEFAULT 8765,
            token TEXT,
            interval INTEGER NOT NULL DEFAULT 3,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS host_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            reachable INTEGER NOT NULL DEFAULT 0,
            error TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            memory_used_bytes INTEGER,
            memory_total_bytes INTEGER,
            upload_bps INTEGER,
            download_bps INTEGER,
            sampled_at REAL,
            FOREIGN KEY(host_id) REFERENCES hosts(id)
        )
    """)

    c.execute("PRAGMA table_info(hosts)")
    host_cols = [row[1] for row in c.fetchall()]
    if 'port' not in host_cols:
        c.execute("ALTER TABLE hosts ADD COLUMN port INTEGER NOT NULL DEFAULT 8765")
    if 'token' not in host_cols:
        c.execute("ALTER TABLE hosts ADD COLUMN token TEXT")
    if 'interval' not in host_cols:
        c.execute("ALTER TABLE hosts ADD COLUMN interval INTEGER NOT NULL DEFAULT 3")
    if 'sort_order' not in host_cols:
        c.execute("ALTER TABLE hosts ADD COLUMN sort_order INTEGER NOT NULL DEFAULT 0")
        c.execute("UPDATE hosts SET sort_order = id")

    c.execute("PRAGMA table_info(host_samples)")
    host_sample_cols = [row[1] for row in c.fetchall()]
    if host_sample_cols and 'sampled_at' not in host_sample_cols:
        c.execute("ALTER TABLE host_samples ADD COLUMN sampled_at REAL")

    conn.commit()
    conn.close()


# --- Drive DB ---

def get_nicknames():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT device, nickname FROM nicknames")
    rows = c.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}


def set_nickname(device, nickname):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if nickname.strip():
        c.execute("INSERT OR REPLACE INTO nicknames (device, nickname) VALUES (?,?)", (device, nickname.strip()))
    else:
        c.execute("DELETE FROM nicknames WHERE device=?", (device,))
    conn.commit()
    conn.close()


def save_snapshot(device, temperature, health, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO snapshots (timestamp, device, temperature, health, data) VALUES (?,?,?,?,?)",
        (datetime.now().isoformat(), device, temperature, health, json.dumps(data))
    )
    conn.commit()
    conn.close()


def get_history(device, limit=48):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, temperature, health FROM snapshots WHERE device=? ORDER BY id DESC LIMIT ?",
        (device, limit)
    )
    rows = c.fetchall()
    conn.close()
    return [{"timestamp": r[0], "temperature": r[1], "health": r[2]} for r in reversed(rows)]


def get_drive_order():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT device FROM drive_order ORDER BY sort_order")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]


def set_drive_order(order):
    if not isinstance(order, list):
        return
    filtered = []
    seen = set()
    ordinal = 1
    for device in order:
        if not isinstance(device, str):
            continue
        device = device.strip()
        if not device or device in seen:
            continue
        seen.add(device)
        filtered.append((device, ordinal))
        ordinal += 1
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM drive_order")
    if filtered:
        c.executemany("INSERT INTO drive_order (device, sort_order) VALUES (?,?)", filtered)
    conn.commit()
    conn.close()


def set_current_devices(devices):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM current_devices")
    if devices:
        c.executemany("INSERT INTO current_devices (device) VALUES (?)", [(d,) for d in devices])
    conn.commit()
    conn.close()


def get_latest_snapshots():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT s.timestamp, s.data
        FROM snapshots s
        JOIN (
            SELECT device, MAX(id) AS max_id
            FROM snapshots
            GROUP BY device
        ) latest ON latest.device = s.device AND latest.max_id = s.id
        JOIN current_devices cd ON cd.device = s.device
        ORDER BY s.device
    """)
    rows = c.fetchall()
    conn.close()
    snapshots = []
    for timestamp, raw_data in rows:
        drive = json.loads(raw_data) if raw_data else {}
        drive["timestamp"] = timestamp
        snapshots.append(drive)
    return snapshots


def get_latest_snapshot_timestamp():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT MAX(timestamp) FROM snapshots WHERE device IN (SELECT device FROM current_devices)")
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] else None


def get_app_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM app_settings WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else default


def set_app_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO app_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value)
    )
    conn.commit()
    conn.close()


def get_debrid_config():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT ip, username, password, updated_at FROM debrid_config WHERE id=1")
    row = c.fetchone()
    conn.close()
    if not row:
        return {}
    return {"ip": row[0] or "", "username": row[1] or "", "password": row[2] or "", "updated_at": row[3]}


def set_debrid_config(ip, username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO debrid_config (id, ip, username, password, updated_at)
        VALUES (1, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            ip=excluded.ip,
            username=excluded.username,
            password=excluded.password,
            updated_at=excluded.updated_at
        """,
        (ip, username, password, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


# --- Services DB ---

def get_all_services():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, url, check_type, interval, chart_window_sec, local_url, local_check_type, created_at FROM services ORDER BY sort_order, id")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "url": r[2], "check_type": r[3], "interval": r[4],
             "chart_window_sec": r[5], "local_url": r[6], "local_check_type": r[7], "created_at": r[8]} for r in rows]


def add_service(name, url, check_type, interval, chart_window_sec, local_url, local_check_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COALESCE(MAX(sort_order), 0) FROM services")
    max_sort = c.fetchone()[0] or 0
    new_sort = max_sort + 1
    c.execute(
        "INSERT INTO services (name, url, check_type, interval, chart_window_sec, local_url, local_check_type, sort_order, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (name, url, check_type, interval, chart_window_sec, local_url or None, local_check_type, new_sort, datetime.now().isoformat())
    )
    service_id = c.lastrowid
    conn.commit()
    conn.close()
    return service_id


def update_service(service_id, name, url, check_type, interval, chart_window_sec, local_url, local_check_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE services SET name=?, url=?, check_type=?, interval=?, chart_window_sec=?, local_url=?, local_check_type=? WHERE id=?",
        (name, url, check_type, interval, chart_window_sec, local_url or None, local_check_type, service_id)
    )
    conn.commit()
    conn.close()


def delete_service(service_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM service_checks WHERE service_id=?", (service_id,))
    c.execute("DELETE FROM services WHERE id=?", (service_id,))
    conn.commit()
    conn.close()


def save_service_check(service_id, status, response_ms, status_code, error, check_target='external'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO service_checks (service_id, timestamp, status, response_ms, status_code, error, check_target) VALUES (?,?,?,?,?,?,?)",
        (service_id, datetime.now().isoformat(), status, response_ms, status_code, error, check_target)
    )
    conn.commit()
    conn.close()


def get_service_history(service_id, limit=90, check_target='external'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, status, response_ms, status_code, error FROM service_checks WHERE service_id=? AND check_target=? ORDER BY id DESC LIMIT ?",
        (service_id, check_target, limit)
    )
    rows = c.fetchall()
    conn.close()
    return [{"timestamp": r[0], "status": r[1], "response_ms": r[2], "status_code": r[3], "error": r[4]} for r in reversed(rows)]


def get_service_latest(service_id, check_target='external'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, status, response_ms, status_code, error FROM service_checks WHERE service_id=? AND check_target=? ORDER BY id DESC LIMIT 1",
        (service_id, check_target)
    )
    row = c.fetchone()
    conn.close()
    if row:
        return {"timestamp": row[0], "status": row[1], "response_ms": row[2], "status_code": row[3], "error": row[4]}
    return None


def get_service_uptime(service_id, limit=100, check_target='external'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT status FROM service_checks WHERE service_id=? AND check_target=? ORDER BY id DESC LIMIT ?",
        (service_id, check_target, limit)
    )
    rows = c.fetchall()
    conn.close()
    if not rows:
        return None
    up = sum(1 for r in rows if r[0] == "up")
    return round((up / len(rows)) * 100, 1)


def save_service_order(order):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for index, service_id in enumerate(order, start=1):
        c.execute("UPDATE services SET sort_order=? WHERE id=?", (index, service_id))
    conn.commit()
    conn.close()


def cleanup_old_service_checks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(days=1)).isoformat()
    c.execute("DELETE FROM service_checks WHERE timestamp < ?", (cutoff,))
    deleted = c.rowcount
    conn.commit()
    conn.close()
    if deleted > 0:
        print(f"  [cleanup] Removed {deleted} expired service check records (>24h old)")


# --- Hosts DB ---

def get_all_hosts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, name, host, port, token, interval, created_at FROM hosts ORDER BY sort_order, id"
    )
    rows = c.fetchall()
    conn.close()
    return [{
        "id": r[0],
        "name": r[1],
        "host": r[2],
        "port": r[3],
        "token": r[4] or "",
        "interval": r[5],
        "created_at": r[6],
    } for r in rows]


def add_host(name, host, port, token, interval):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COALESCE(MAX(sort_order), 0) FROM hosts")
    max_sort = c.fetchone()[0] or 0
    c.execute(
        "INSERT INTO hosts (name, host, port, token, interval, sort_order, created_at) VALUES (?,?,?,?,?,?,?)",
        (name, host, int(port), token or None, int(interval), max_sort + 1, datetime.now().isoformat())
    )
    host_id = c.lastrowid
    conn.commit()
    conn.close()
    return host_id


def update_host(host_id, name, host, port, token, interval):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE hosts SET name=?, host=?, port=?, token=?, interval=? WHERE id=?",
        (name, host, int(port), token or None, int(interval), host_id)
    )
    conn.commit()
    conn.close()


def delete_host(host_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM host_samples WHERE host_id=?", (host_id,))
    c.execute("DELETE FROM hosts WHERE id=?", (host_id,))
    conn.commit()
    conn.close()


def save_host_order(order):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for index, host_id in enumerate(order, start=1):
        c.execute("UPDATE hosts SET sort_order=? WHERE id=?", (index, host_id))
    conn.commit()
    conn.close()


def save_host_sample(host_id, reachable, error=None, stats=None):
    stats = stats or {}
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO host_samples (
            host_id, timestamp, reachable, error, cpu_percent, memory_percent,
            memory_used_bytes, memory_total_bytes, upload_bps, download_bps, sampled_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            host_id,
            datetime.now().isoformat(),
            1 if reachable else 0,
            error,
            stats.get("cpu_percent"),
            stats.get("memory_percent"),
            stats.get("memory_used_bytes"),
            stats.get("memory_total_bytes"),
            stats.get("upload_bps"),
            stats.get("download_bps"),
            stats.get("sampled_at"),
        )
    )
    conn.commit()
    conn.close()


def get_host_latest_sample(host_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT timestamp, reachable, error, cpu_percent, memory_percent, memory_used_bytes,
               memory_total_bytes, upload_bps, download_bps, sampled_at
        FROM host_samples
        WHERE host_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (host_id,)
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "timestamp": row[0],
        "reachable": bool(row[1]),
        "error": row[2],
        "cpu_percent": row[3],
        "memory_percent": row[4],
        "memory_used_bytes": row[5],
        "memory_total_bytes": row[6],
        "upload_bps": row[7],
        "download_bps": row[8],
        "sampled_at": row[9],
    }


def get_host_history(host_id, window_sec=60, limit=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(seconds=max(1, int(window_sec)))).isoformat()
    query = """
        SELECT timestamp, reachable, error, cpu_percent, memory_percent, upload_bps, download_bps
        FROM host_samples
        WHERE host_id=? AND timestamp >= ?
        ORDER BY id ASC
    """
    params = [host_id, cutoff]
    if limit is not None:
        query += " LIMIT ?"
        params.append(int(limit))
    c.execute(query, tuple(params))
    rows = c.fetchall()
    conn.close()
    return [{
        "timestamp": r[0],
        "reachable": bool(r[1]),
        "error": r[2],
        "cpu_percent": r[3],
        "memory_percent": r[4],
        "upload_bps": r[5],
        "download_bps": r[6],
    } for r in rows]


def cleanup_old_host_samples():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=1)).isoformat()
    c.execute("DELETE FROM host_samples WHERE timestamp < ?", (cutoff,))
    deleted = c.rowcount
    conn.commit()
    conn.close()
    if deleted > 0:
        print(f"  [cleanup] Removed {deleted} expired host sample records (>1h old)")
