from html import escape

TYPE_ID = "rdt_client"
LABEL = "RDT Client"
META = "Active torrent queue"
DEFAULT_TITLE = LABEL

CSS = r"""
.overview-debrid-header {
  gap: 12px;
}
.overview-debrid-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}
.overview-debrid-magnet-link {
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
.overview-debrid-magnet-link:hover {
  color: var(--accent);
}
.overview-debrid-magnet-link:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 4px;
}
.overview-debrid-magnet-link .material-icons {
  font-size: 18px;
  line-height: 1;
}
.overview-debrid-status {
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.overview-debrid-magnet-status {
  font-size: 11px;
  color: var(--muted);
  min-height: 16px;
  margin-bottom: 10px;
}
.overview-debrid-magnet-status:empty {
  margin-bottom: 0;
  min-height: 0;
}
.overview-debrid-magnet-status.success {
  color: var(--pass);
}
.overview-debrid-magnet-status.error {
  color: var(--fail);
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
          <div class="panel-header overview-debrid-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">download</span>
              <button class="panel-title panel-title-button" type="button" onclick="renameOverviewWidget('{instance_id}')" title="Rename widget">{title}</button>
            </div>
            <div class="overview-debrid-actions">
              <button class="overview-debrid-magnet-link" type="button" onclick="openOverviewDebridMagnetModal()" title="Queue magnet link" aria-label="Queue magnet link">
                <span class="material-icons" aria-hidden="true">link</span>
              </button>
              <button class="panel-link" onclick="navigate('debrid')">View all →</button>
            </div>
          </div>
          <div class="panel-body">
            <div class="overview-debrid-status" data-role="overview-debrid-status">Loading queue…</div>
            <div class="overview-debrid-magnet-status" data-role="overview-debrid-magnet-status" aria-live="polite"></div>
            <div class="overview-debrid-list" data-widget-slot="{TYPE_ID}">
              <div class="loading"><div class="loading-spinner"></div></div>
            </div>
          </div>
        </div>
"""
