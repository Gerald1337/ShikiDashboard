from html import escape

TYPE_ID = "host_resources"
LABEL = "Host Resource Statistics"
META = "CPU, RAM, and network activity snapshot"
DEFAULT_TITLE = LABEL

CSS = r"""
.host-panel-header {
  gap: 12px;
}
.host-panel-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}
.host-panel-settings-btn {
  border: none;
  background: none;
  color: var(--muted);
  padding: 0;
  margin: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  line-height: 1;
  flex: 0 0 auto;
}
.host-panel-settings-btn:hover {
  color: var(--accent);
}
.host-panel-settings-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 4px;
}
.host-panel-settings-btn .material-icons {
  font-size: 18px;
  line-height: 1;
}
.host-panel-status {
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
  margin-bottom: 10px;
}
.host-stats-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.host-stat-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  padding: 8px 0;
  gap: 12px;
}
.host-stat-row:last-child {
  border-bottom: none;
}
.host-stat-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}
.host-stat-value-group {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  text-align: right;
  gap: 2px;
}
.host-stat-value {
  font-size: 13px;
  font-weight: 600;
  line-height: 1;
}
.host-stat-sub {
  font-size: 11px;
  color: var(--muted);
}
"""


def render_widget(instance):
  instance_id = escape(instance["instance_id"], quote=True)
  title = escape((instance.get("title") or DEFAULT_TITLE).strip())
  config = instance.get("config") or {}
  selected_host_id = config.get("host_id", 0)
  try:
    selected_host_id = int(selected_host_id)
  except (TypeError, ValueError):
    selected_host_id = 0
  if selected_host_id < 0:
    selected_host_id = 0
  return f"""
        <div class="overview-panel host-panel" data-widget-type="{TYPE_ID}" data-widget-instance="{instance_id}" data-selected-host-id="{selected_host_id}">
          <div class="panel-header host-panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">monitor_heart</span>
              <button class="panel-title panel-title-button" type="button" onclick="renameOverviewWidget('{instance_id}')" title="Rename widget">{title}</button>
            </div>
            <div class="host-panel-actions">
              <button class="host-panel-settings-btn" type="button" onclick="openOverviewHostWidgetModal('{instance_id}')" title="Choose host" aria-label="Choose host">
                <span class="material-icons" aria-hidden="true">settings</span>
              </button>
            </div>
          </div>
          <div class="panel-body">
            <div class="host-panel-status" data-role="host-panel-status">Loading host…</div>
            <div class="host-stats-list">
              <div class="host-stat-row">
                <div class="host-stat-label">CPU</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" data-role="cpu-value">—</div>
                  <div class="host-stat-sub" data-role="cpu-sub">—</div>
                </div>
              </div>
              <div class="host-stat-row">
                <div class="host-stat-label">RAM</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" data-role="ram-value">—</div>
                  <div class="host-stat-sub" data-role="ram-sub">—</div>
                </div>
              </div>
              <div class="host-stat-row">
                <div class="host-stat-label">Upload</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" data-role="upload-value">—</div>
                  <div class="host-stat-sub" data-role="upload-sub">—</div>
                </div>
              </div>
              <div class="host-stat-row">
                <div class="host-stat-label">Download</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" data-role="download-value">—</div>
                  <div class="host-stat-sub" data-role="download-sub">—</div>
                </div>
              </div>
            </div>
          </div>
        </div>
"""
