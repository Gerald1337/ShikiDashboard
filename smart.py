import json
import subprocess
from config import IS_MAC, MOCK_DRIVES
from db import save_snapshot


def generate_mock_smart_data(drive):
    attrs = [
        {"id": 1, "name": "Read Error Rate", "value": 100, "worst": 100, "thresh": 6, "raw": 0, "failed": False},
        {"id": 3, "name": "Spin Up Time", "value": 100, "worst": 100, "thresh": 0, "raw": 0, "failed": False},
        {"id": 4, "name": "Start Stop Count", "value": 95, "worst": 95, "thresh": 20, "raw": 185, "failed": False},
        {"id": 5, "name": "Reallocated Sectors Count", "value": 100, "worst": 100, "thresh": 10, "raw": 0, "failed": False},
        {"id": 7, "name": "Seek Error Rate", "value": 100, "worst": 100, "thresh": 30, "raw": 0, "failed": False},
        {"id": 9, "name": "Power On Hours", "value": 80, "worst": 80, "thresh": 0, "raw": drive["power_on_hours"], "failed": False},
        {"id": 10, "name": "Spin Retry Count", "value": 100, "worst": 100, "thresh": 97, "raw": 0, "failed": False},
        {"id": 12, "name": "Power Cycle Count", "value": 98, "worst": 98, "thresh": 20, "raw": 45, "failed": False},
        {"id": 192, "name": "Power Off Retract Count", "value": 100, "worst": 100, "thresh": 0, "raw": 12, "failed": False},
        {"id": 193, "name": "Load Cycle Count", "value": 99, "worst": 99, "thresh": 0, "raw": 2345, "failed": False},
        {"id": 194, "name": "Temperature Celsius", "value": 100, "worst": 100, "thresh": 0, "raw": drive["temperature"], "failed": False},
        {"id": 196, "name": "Reallocated Event Count", "value": 100, "worst": 100, "thresh": 0, "raw": 0, "failed": False},
        {"id": 197, "name": "Current Pending Sector", "value": 100, "worst": 100, "thresh": 0, "raw": 0, "failed": False},
        {"id": 199, "name": "UDMA CRC Error Count", "value": 100, "worst": 100, "thresh": 0, "raw": 0, "failed": False},
        {"id": 200, "name": "Write Error Rate", "value": 100, "worst": 100, "thresh": 0, "raw": 0, "failed": False},
    ]

    return {
        "device": {"name": drive["name"]},
        "model_name": drive["model"],
        "serial_number": drive["serial"],
        "firmware_version": drive["firmware"],
        "rotation_rate": 0 if drive["drive_type"] == "SSD" else 7200,
        "user_capacity": {"bytes": drive["capacity_gb"] * 1024**3},
        "temperature": {"current": drive["temperature"]},
        "power_on_time": {"hours": drive["power_on_hours"]},
        "smart_status": {"passed": drive["health"] == "PASS"},
        "ata_smart_attributes": {"table": attrs},
    }


def get_drives():
    if IS_MAC:
        return MOCK_DRIVES
    try:
        result = subprocess.run(["smartctl", "--scan"], capture_output=True, text=True, timeout=10)
        drives = []
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 3 and parts[1] == "-d":
                drives.append({"name": parts[0], "type": parts[2]})
            elif parts:
                drives.append({"name": parts[0], "type": None})
        return drives
    except Exception:
        return []


def get_smart_data(device_name, device_type=None):
    if IS_MAC:
        for drive in MOCK_DRIVES:
            if drive["name"] == device_name:
                return generate_mock_smart_data(drive)
        return {"error": "Device not found"}

    try:
        cmd = ["smartctl", "-a", "-j"]
        if device_type and device_type not in ("auto",):
            cmd += ["-d", device_type]
        cmd.append(device_name)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}


def parse_drive(device):
    if isinstance(device, dict):
        device_name = device["name"]
        device_type = device.get("type")
    else:
        device_name = device
        device_type = None

    raw = get_smart_data(device_name, device_type)
    device = device_name

    if "error" in raw and not raw.get("smart_status"):
        return {"device": device, "error": raw["error"], "health": "UNKNOWN"}

    info = raw.get("device", {})
    smart_status = raw.get("smart_status", {})
    health = "PASS" if smart_status.get("passed", False) else "FAIL"

    temp = None
    temp_obj = raw.get("temperature", {})
    if temp_obj:
        temp = temp_obj.get("current")

    model = raw.get("model_name", raw.get("scsi_model_name", "Unknown"))
    serial = raw.get("serial_number", "Unknown")
    capacity_raw = raw.get("user_capacity", {})
    capacity_bytes = capacity_raw.get("bytes", 0) if isinstance(capacity_raw, dict) else 0
    capacity_gb = round(capacity_bytes / (1024**3), 1) if capacity_bytes else None

    firmware = raw.get("firmware_version", "Unknown")
    rotation = raw.get("rotation_rate", None)
    drive_type = "SSD" if rotation == 0 else ("HDD" if rotation else info.get("type", "Unknown").upper())

    power_hours = raw.get("power_on_time", {}).get("hours", None)

    attributes = []
    ata_attrs = raw.get("ata_smart_attributes", {}).get("table", [])
    for attr in ata_attrs:
        attributes.append({
            "id": attr.get("id"),
            "name": attr.get("name", "").replace("_", " ").title(),
            "value": attr.get("value"),
            "worst": attr.get("worst"),
            "thresh": attr.get("thresh"),
            "raw": attr.get("raw", {}).get("value") if isinstance(attr.get("raw"), dict) else attr.get("raw"),
            "failed": attr.get("when_failed", "") not in ("", "-"),
        })

    nvme_log = raw.get("nvme_smart_health_information_log", {})
    if nvme_log:
        nvme_map = {
            "critical_warning": "Critical Warning",
            "temperature": "Temperature",
            "available_spare": "Available Spare %",
            "available_spare_threshold": "Spare Threshold %",
            "percentage_used": "% Life Used",
            "data_units_read": "Data Units Read",
            "data_units_written": "Data Units Written",
            "power_cycles": "Power Cycles",
            "power_on_hours": "Power On Hours",
            "unsafe_shutdowns": "Unsafe Shutdowns",
            "media_errors": "Media Errors",
        }
        for key, label in nvme_map.items():
            val = nvme_log.get(key)
            if val is not None:
                attributes.append({"id": None, "name": label, "value": val, "worst": None, "thresh": None, "raw": val, "failed": False})

    drive = {
        "device": device,
        "model": model,
        "serial": serial,
        "firmware": firmware,
        "type": drive_type,
        "capacity_gb": capacity_gb,
        "health": health,
        "temperature": temp,
        "power_on_hours": power_hours,
        "attributes": attributes,
    }
    save_snapshot(device, temp, health, drive)
    return drive


def scan_all_drives():
    devices = get_drives()
    drives = [parse_drive(dev) for dev in devices]
    meaningful = [d for d in drives if d.get("model", "Unknown") != "Unknown" or d.get("temperature") is not None]
    return meaningful if meaningful else drives
