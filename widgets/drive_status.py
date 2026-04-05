from html import escape

TYPE_ID = "drive_status"
LABEL = "Drive Status"
META = "Temperature and health overview"
DEFAULT_TITLE = LABEL

CSS = r"""
.overview-drive-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.overview-drive-row:last-child {
  border-bottom: none;
}
.overview-drive-name {
  font-weight: 500;
}
.overview-drive-meta {
  color: var(--muted);
  font-size: 11px;
  margin-top: 2px;
}
"""


def render_widget(instance):
  instance_id = escape(instance["instance_id"], quote=True)
  title = escape((instance.get("title") or DEFAULT_TITLE).strip())
  return f"""
        <div class="overview-panel" data-widget-type="{TYPE_ID}" data-widget-instance="{instance_id}">
          <div class="panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">storage</span>
              <button class="panel-title panel-title-button" type="button" onclick="renameOverviewWidget('{instance_id}')" title="Rename widget">{title}</button>
            </div>
            <button class="panel-link" onclick="navigate('disks')">View all →</button>
          </div>
          <div class="panel-body" data-widget-slot="{TYPE_ID}">
            <div class="loading"><div class="loading-spinner"></div></div>
          </div>
        </div>
"""
