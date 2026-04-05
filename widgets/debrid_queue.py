from html import escape

TYPE_ID = "debrid_queue"
LABEL = "Debrid Queue"
META = "Active torrent queue"
DEFAULT_TITLE = LABEL

CSS = r"""
.overview-debrid-status {
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.overview-debrid-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.overview-debrid-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.02);
}
.overview-debrid-name {
  font-size: 13px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.overview-debrid-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.overview-debrid-meta-right {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-end;
  flex-wrap: wrap;
}
"""


def render_widget(instance):
  instance_id = escape(instance["instance_id"], quote=True)
  title = escape((instance.get("title") or DEFAULT_TITLE).strip())
  return f"""
        <div class="overview-panel" data-widget-type="{TYPE_ID}" data-widget-instance="{instance_id}">
          <div class="panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">download</span>
              <button class="panel-title panel-title-button" type="button" onclick="renameOverviewWidget('{instance_id}')" title="Rename widget">{title}</button>
            </div>
            <button class="panel-link" onclick="navigate('debrid')">View all →</button>
          </div>
          <div class="panel-body">
            <div class="overview-debrid-status" data-role="overview-debrid-status">Loading queue…</div>
            <div class="overview-debrid-list" data-widget-slot="{TYPE_ID}">
              <div class="loading"><div class="loading-spinner"></div></div>
            </div>
          </div>
        </div>
"""
