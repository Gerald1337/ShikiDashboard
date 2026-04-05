from copy import deepcopy
import re

from .debrid_queue import (
    CSS as DEBRID_QUEUE_WIDGET_CSS,
    DEFAULT_TITLE as DEBRID_QUEUE_WIDGET_DEFAULT_TITLE,
    LABEL as DEBRID_QUEUE_WIDGET_LABEL,
    META as DEBRID_QUEUE_WIDGET_META,
    TYPE_ID as DEBRID_QUEUE_WIDGET_TYPE,
    render_widget as render_debrid_queue_widget,
)
from .drive_status import (
    CSS as DRIVE_STATUS_WIDGET_CSS,
    DEFAULT_TITLE as DRIVE_STATUS_WIDGET_DEFAULT_TITLE,
    LABEL as DRIVE_STATUS_WIDGET_LABEL,
    META as DRIVE_STATUS_WIDGET_META,
    TYPE_ID as DRIVE_STATUS_WIDGET_TYPE,
    render_widget as render_drive_status_widget,
)
from .host_resources import (
    CSS as HOST_RESOURCES_WIDGET_CSS,
    DEFAULT_TITLE as HOST_RESOURCES_WIDGET_DEFAULT_TITLE,
    LABEL as HOST_RESOURCES_WIDGET_LABEL,
    META as HOST_RESOURCES_WIDGET_META,
    TYPE_ID as HOST_RESOURCES_WIDGET_TYPE,
    render_widget as render_host_resources_widget,
)
from .service_status import (
    CSS as SERVICE_STATUS_WIDGET_CSS,
    DEFAULT_TITLE as SERVICE_STATUS_WIDGET_DEFAULT_TITLE,
    LABEL as SERVICE_STATUS_WIDGET_LABEL,
    META as SERVICE_STATUS_WIDGET_META,
    TYPE_ID as SERVICE_STATUS_WIDGET_TYPE,
    render_widget as render_service_status_widget,
)

INSTANCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

WIDGET_TYPES = {
    HOST_RESOURCES_WIDGET_TYPE: {
        "label": HOST_RESOURCES_WIDGET_LABEL,
        "meta": HOST_RESOURCES_WIDGET_META,
        "default_title": HOST_RESOURCES_WIDGET_DEFAULT_TITLE,
        "render": render_host_resources_widget,
        "css": HOST_RESOURCES_WIDGET_CSS,
    },
    SERVICE_STATUS_WIDGET_TYPE: {
        "label": SERVICE_STATUS_WIDGET_LABEL,
        "meta": SERVICE_STATUS_WIDGET_META,
        "default_title": SERVICE_STATUS_WIDGET_DEFAULT_TITLE,
        "render": render_service_status_widget,
        "css": SERVICE_STATUS_WIDGET_CSS,
    },
    DRIVE_STATUS_WIDGET_TYPE: {
        "label": DRIVE_STATUS_WIDGET_LABEL,
        "meta": DRIVE_STATUS_WIDGET_META,
        "default_title": DRIVE_STATUS_WIDGET_DEFAULT_TITLE,
        "render": render_drive_status_widget,
        "css": DRIVE_STATUS_WIDGET_CSS,
    },
    DEBRID_QUEUE_WIDGET_TYPE: {
        "label": DEBRID_QUEUE_WIDGET_LABEL,
        "meta": DEBRID_QUEUE_WIDGET_META,
        "default_title": DEBRID_QUEUE_WIDGET_DEFAULT_TITLE,
        "render": render_debrid_queue_widget,
        "css": DEBRID_QUEUE_WIDGET_CSS,
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
        "instance_id": "host_resources_main",
        "type": HOST_RESOURCES_WIDGET_TYPE,
        "title": HOST_RESOURCES_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
    {
        "instance_id": "service_status_main",
        "type": SERVICE_STATUS_WIDGET_TYPE,
        "title": SERVICE_STATUS_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
    {
        "instance_id": "drive_status_main",
        "type": DRIVE_STATUS_WIDGET_TYPE,
        "title": DRIVE_STATUS_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
    {
        "instance_id": "debrid_queue_main",
        "type": DEBRID_QUEUE_WIDGET_TYPE,
        "title": DEBRID_QUEUE_WIDGET_DEFAULT_TITLE,
        "config": {},
    },
]

LEGACY_OVERVIEW_PANEL_TYPE_MAP = {
    "host": HOST_RESOURCES_WIDGET_TYPE,
    "services": SERVICE_STATUS_WIDGET_TYPE,
    "drives": DRIVE_STATUS_WIDGET_TYPE,
    "debrid": DEBRID_QUEUE_WIDGET_TYPE,
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
        type_id = item.get("type")
        if type_id not in WIDGET_TYPES:
            continue
        instance_id = _sanitize_instance_id(item.get("instance_id"))
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
