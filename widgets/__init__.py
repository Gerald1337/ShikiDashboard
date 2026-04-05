from copy import deepcopy
import re

from .rdt_client import (
    CSS as RDT_CLIENT_WIDGET_CSS,
    DEFAULT_TITLE as RDT_CLIENT_WIDGET_DEFAULT_TITLE,
    LABEL as RDT_CLIENT_WIDGET_LABEL,
    META as RDT_CLIENT_WIDGET_META,
    TYPE_ID as RDT_CLIENT_WIDGET_TYPE,
    render_widget as render_rdt_client_widget,
)
from .drive_monitor import (
    CSS as DRIVE_MONITOR_WIDGET_CSS,
    DEFAULT_TITLE as DRIVE_MONITOR_WIDGET_DEFAULT_TITLE,
    LABEL as DRIVE_MONITOR_WIDGET_LABEL,
    META as DRIVE_MONITOR_WIDGET_META,
    TYPE_ID as DRIVE_MONITOR_WIDGET_TYPE,
    render_widget as render_drive_monitor_widget,
)
from .resource_monitor import (
    CSS as RESOURCE_MONITOR_WIDGET_CSS,
    DEFAULT_TITLE as RESOURCE_MONITOR_WIDGET_DEFAULT_TITLE,
    LABEL as RESOURCE_MONITOR_WIDGET_LABEL,
    META as RESOURCE_MONITOR_WIDGET_META,
    TYPE_ID as RESOURCE_MONITOR_WIDGET_TYPE,
    render_widget as render_resource_monitor_widget,
)
from .service_monitor import (
    CSS as SERVICE_MONITOR_WIDGET_CSS,
    DEFAULT_TITLE as SERVICE_MONITOR_WIDGET_DEFAULT_TITLE,
    LABEL as SERVICE_MONITOR_WIDGET_LABEL,
    META as SERVICE_MONITOR_WIDGET_META,
    TYPE_ID as SERVICE_MONITOR_WIDGET_TYPE,
    render_widget as render_service_monitor_widget,
)
from .emby import (
    CSS as EMBY_WIDGET_CSS,
    DEFAULT_TITLE as EMBY_WIDGET_DEFAULT_TITLE,
    LABEL as EMBY_WIDGET_LABEL,
    META as EMBY_WIDGET_META,
    TYPE_ID as EMBY_WIDGET_TYPE,
    render_widget as render_emby_widget,
)

INSTANCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

WIDGET_TYPES = {
    RESOURCE_MONITOR_WIDGET_TYPE: {
        "label": RESOURCE_MONITOR_WIDGET_LABEL,
        "meta": RESOURCE_MONITOR_WIDGET_META,
        "default_title": RESOURCE_MONITOR_WIDGET_DEFAULT_TITLE,
        "render": render_resource_monitor_widget,
        "css": RESOURCE_MONITOR_WIDGET_CSS,
    },
    SERVICE_MONITOR_WIDGET_TYPE: {
        "label": SERVICE_MONITOR_WIDGET_LABEL,
        "meta": SERVICE_MONITOR_WIDGET_META,
        "default_title": SERVICE_MONITOR_WIDGET_DEFAULT_TITLE,
        "render": render_service_monitor_widget,
        "css": SERVICE_MONITOR_WIDGET_CSS,
    },
    DRIVE_MONITOR_WIDGET_TYPE: {
        "label": DRIVE_MONITOR_WIDGET_LABEL,
        "meta": DRIVE_MONITOR_WIDGET_META,
        "default_title": DRIVE_MONITOR_WIDGET_DEFAULT_TITLE,
        "render": render_drive_monitor_widget,
        "css": DRIVE_MONITOR_WIDGET_CSS,
    },
    RDT_CLIENT_WIDGET_TYPE: {
        "label": RDT_CLIENT_WIDGET_LABEL,
        "meta": RDT_CLIENT_WIDGET_META,
        "default_title": RDT_CLIENT_WIDGET_DEFAULT_TITLE,
        "render": render_rdt_client_widget,
        "css": RDT_CLIENT_WIDGET_CSS,
    },
    EMBY_WIDGET_TYPE: {
        "label": EMBY_WIDGET_LABEL,
        "meta": EMBY_WIDGET_META,
        "default_title": EMBY_WIDGET_DEFAULT_TITLE,
        "render": render_emby_widget,
        "css": EMBY_WIDGET_CSS,
    },
}

OVERVIEW_WIDGET_TYPE_METADATA = {
    type_id: {
        "label": definition["label"],
        "meta": definition["meta"],
    }
    for type_id, definition in WIDGET_TYPES.items()
}

DEFAULT_OVERVIEW_WIDGET_LAYOUT = [
    {
        "instance_id": "resource_monitor_main",
        "type": RESOURCE_MONITOR_WIDGET_TYPE,
        "title": RESOURCE_MONITOR_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
    {
        "instance_id": "service_monitor_main",
        "type": SERVICE_MONITOR_WIDGET_TYPE,
        "title": SERVICE_MONITOR_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
    {
        "instance_id": "drive_monitor_main",
        "type": DRIVE_MONITOR_WIDGET_TYPE,
        "title": DRIVE_MONITOR_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
    {
        "instance_id": "rdt_client_main",
        "type": RDT_CLIENT_WIDGET_TYPE,
        "title": RDT_CLIENT_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
    {
        "instance_id": "emby_main",
        "type": EMBY_WIDGET_TYPE,
        "title": EMBY_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
]

LEGACY_OVERVIEW_PANEL_TYPE_MAP = {
    "host": RESOURCE_MONITOR_WIDGET_TYPE,
    "services": SERVICE_MONITOR_WIDGET_TYPE,
    "drives": DRIVE_MONITOR_WIDGET_TYPE,
    "debrid": RDT_CLIENT_WIDGET_TYPE,
    "host_resources": RESOURCE_MONITOR_WIDGET_TYPE,
    "service_status": SERVICE_MONITOR_WIDGET_TYPE,
    "drive_status": DRIVE_MONITOR_WIDGET_TYPE,
    "debrid_queue": RDT_CLIENT_WIDGET_TYPE,
}

LEGACY_OVERVIEW_WIDGET_INSTANCE_MAP = {
    "host_resources_main": "resource_monitor_main",
    "service_status_main": "service_monitor_main",
    "drive_status_main": "drive_monitor_main",
    "debrid_queue_main": "rdt_client_main",
}

OVERVIEW_WIDGET_STYLES = "\n".join(
    definition["css"].strip()
    for definition in WIDGET_TYPES.values()
    if definition["css"].strip()
)


def _sanitize_instance_id(value):
    if not isinstance(value, str):
        return ""
    normalized = value.strip()
    return normalized if INSTANCE_ID_PATTERN.fullmatch(normalized) else ""


def _clone_widget_instance(widget):
    config = widget.get("config")
    return {
        "instance_id": widget["instance_id"],
        "type": widget["type"],
        "title": widget["title"],
        "config": deepcopy(config) if isinstance(config, dict) else {},
    }


def default_overview_widget_layout():
    return [_clone_widget_instance(widget) for widget in DEFAULT_OVERVIEW_WIDGET_LAYOUT]


def _default_widget_by_type():
    defaults = {}
    for widget in DEFAULT_OVERVIEW_WIDGET_LAYOUT:
        defaults.setdefault(widget["type"], widget)
    return defaults


def sanitize_overview_widget_layout(layout):
    default_layout = default_overview_widget_layout()
    default_by_instance = {widget["instance_id"]: widget for widget in default_layout}
    default_by_type = _default_widget_by_type()

    if not isinstance(layout, list):
        return default_layout

    if not layout:
        return []

    if layout and all(isinstance(item, str) for item in layout):
        sanitized = []
        seen = set()
        for item in layout:
            widget = default_by_instance.get(item)
            if widget is None:
                widget = default_by_instance.get(LEGACY_OVERVIEW_WIDGET_INSTANCE_MAP.get(item, ""))
            if widget is None:
                widget = default_by_type.get(LEGACY_OVERVIEW_PANEL_TYPE_MAP.get(item))
            if widget and widget["instance_id"] not in seen:
                sanitized.append(_clone_widget_instance(widget))
                seen.add(widget["instance_id"])
        for widget in default_layout:
            if widget["instance_id"] not in seen:
                sanitized.append(_clone_widget_instance(widget))
        return sanitized or default_layout

    sanitized = []
    seen = set()
    for item in layout:
        if not isinstance(item, dict):
            continue
        type_id = LEGACY_OVERVIEW_PANEL_TYPE_MAP.get(item.get("type"), item.get("type"))
        if type_id not in WIDGET_TYPES:
            continue
        instance_id = _sanitize_instance_id(item.get("instance_id"))
        instance_id = LEGACY_OVERVIEW_WIDGET_INSTANCE_MAP.get(instance_id, instance_id)
        if not instance_id or instance_id in seen:
            continue
        default_widget = default_by_type.get(type_id)
        default_title = (
            default_widget["title"]
            if default_widget
            else WIDGET_TYPES[type_id]["default_title"]
        )
        title = item.get("title")
        config = item.get("config")
        sanitized.append({
            "instance_id": instance_id,
            "type": type_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else default_title,
            "config": deepcopy(config) if isinstance(config, dict) else {},
        })
        seen.add(instance_id)

    return sanitized


def render_overview_widgets(layout=None):
    sanitized_layout = sanitize_overview_widget_layout(layout)
    rendered = []
    for widget in sanitized_layout:
        rendered.append(WIDGET_TYPES[widget["type"]]["render"](widget))
    return "\n".join(rendered)
