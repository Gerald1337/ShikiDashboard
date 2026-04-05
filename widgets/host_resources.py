from html import escape

TYPE_ID = "host_resources"
LABEL = "Host Resource Statistics"
META = "CPU, RAM, and network activity snapshot"
DEFAULT_TITLE = LABEL

CSS = r"""
.host-panel-status {
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
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
  return f"""
        <div class="overview-panel host-panel" data-widget-type="{TYPE_ID}" data-widget-instance="{instance_id}">
          <div class="panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">monitor_heart</span>
              <button class="panel-title panel-title-button" type="button" onclick="renameOverviewWidget('{instance_id}')" title="Rename widget">{title}</button>
            </div>
          </div>
          <div class="panel-body">
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
