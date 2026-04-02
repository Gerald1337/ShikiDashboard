import os
import sys

IS_MAC = sys.platform == "darwin"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diskwatch.db")

MOCK_DRIVES = [
    {
        "name": "/dev/disk0",
        "type": None,
        "model": "Apple SSD SM1024L",
        "serial": "S69345L200001",
        "firmware": "4B241101",
        "drive_type": "SSD",
        "capacity_gb": 1024,
        "temperature": 38,
        "health": "PASS",
        "power_on_hours": 4320,
    },
    {
        "name": "/dev/disk1",
        "type": None,
        "model": "Samsung 870 QVO",
        "serial": "S5Y7NF0T654321",
        "firmware": "SVT05B6Q",
        "drive_type": "SSD",
        "capacity_gb": 2048,
        "temperature": 42,
        "health": "PASS",
        "power_on_hours": 8760,
    },
    {
        "name": "/dev/disk2",
        "type": None,
        "model": "WDC WD40EZRZ-00GXCB0",
        "serial": "WD-WCC7K6XXXXXXXXXXX",
        "firmware": "80.0",
        "drive_type": "HDD",
        "capacity_gb": 4096,
        "temperature": 35,
        "health": "PASS",
        "power_on_hours": 24000,
    },
    {
        "name": "/dev/disk3",
        "type": None,
        "model": "Seagate Barracuda Pro",
        "serial": "ZR268KWF",
        "firmware": "CC97",
        "drive_type": "HDD",
        "capacity_gb": 8192,
        "temperature": 45,
        "health": "PASS",
        "power_on_hours": 18500,
    },
]

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

REACHABLE_CODES = {200, 201, 204, 301, 302, 304, 307, 308, 401, 403, 405, 429}
