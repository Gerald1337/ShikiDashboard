from html import escape

TYPE_ID = "service_monitor"
LABEL = "Service Monitor"
META = "External and local health summary"
DEFAULT_TITLE = LABEL

CSS = r"""
.overview-service-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.overview-service-row:last-child {
  border-bottom: none;
}
"""


def render_widget(instance):
  instance_id = escape(instance["instance_id"], quote=True)
  title = escape((instance.get("title") or DEFAULT_TITLE).strip())
  return f"""
        <div class="overview-panel" data-widget-type="{TYPE_ID}" data-widget-instance="{instance_id}">
          <div class="panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">public</span>
              <button class="panel-title panel-title-button" type="button" onclick="renameOverviewWidget('{instance_id}')" title="Rename widget">{title}</button>
            </div>
            <button class="panel-link" onclick="navigate('services')">View all →</button>
          </div>
          <div class="panel-body" data-widget-slot="{TYPE_ID}">
            <div class="loading"><div class="loading-spinner"></div></div>
          </div>
        </div>
"""
