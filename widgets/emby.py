from html import escape

TYPE_ID = "emby"
LABEL = "Emby"
META = "Active playback and latest additions"
DEFAULT_TITLE = LABEL

CSS = r"""
.emby-panel-header {
  gap: 12px;
}
.emby-panel-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}
.emby-panel-health {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 12px;
}
.emby-panel-title-row {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.emby-panel-settings-btn {
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
.emby-panel-settings-btn:hover {
  color: var(--accent);
}
.emby-panel-settings-btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 4px;
}
.emby-panel-settings-btn .material-icons {
  font-size: 18px;
  line-height: 1;
}
.emby-panel-status {
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
  margin-bottom: 8px;
}
.emby-panel-status:empty {
  display: none;
  margin-bottom: 0;
}
.emby-panel-backup-status {
  font-size: 11px;
  color: var(--muted);
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-bottom: 12px;
}
.emby-panel-backup-status.is-stale {
  color: #ff6b6b;
}
.emby-panel-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.emby-panel-section.is-hidden {
  display: none;
}
.emby-panel-section + .emby-panel-section {
  margin-top: 14px;
}
.emby-panel-section-title {
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.emby-panel-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.emby-panel-list.recent-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.emby-panel-card {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.02);
}
.emby-panel-card-content {
  flex: 1 1 auto;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.emby-panel-card-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
}
.emby-panel-card-poster {
  width: 48px;
  height: 72px;
  border-radius: 8px;
  object-fit: cover;
  flex: 0 0 auto;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
}
.emby-panel-avatar {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  object-fit: cover;
  flex: 0 0 auto;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
}
.emby-panel-session-header {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: space-between;
}
.emby-panel-session-progress-label {
  font-size: 11px;
  color: var(--muted);
  white-space: nowrap;
}
.emby-panel-progress {
  width: 100%;
  height: 6px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.08);
  margin-top: 4px;
}
.emby-panel-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), #7af0ff);
  border-radius: inherit;
}
.emby-panel-card-meta {
  font-size: 11px;
  color: var(--muted);
  line-height: 1.4;
}
.emby-panel-empty {
  font-size: 12px;
  color: var(--muted);
  padding: 10px 0;
}
"""


def render_widget(instance):
    instance_id = escape(instance["instance_id"], quote=True)
    title = escape((instance.get("title") or DEFAULT_TITLE).strip())
    return f"""
        <div class="overview-panel" data-widget-type="{TYPE_ID}" data-widget-instance="{instance_id}">
          <div class="panel-header emby-panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">live_tv</span>
              <div class="emby-panel-title-row">
                <button class="panel-title panel-title-button" type="button" onclick="renameOverviewWidget('{instance_id}')" title="Rename widget">{title}</button>
                <span class="emby-panel-health" data-role="emby-health-indicator" title="Checking Emby server status" aria-label="Checking Emby server status">
                  <span class="status-dot unknown" aria-hidden="true"></span>
                </span>
              </div>
            </div>
            <div class="emby-panel-actions">
              <button class="emby-panel-settings-btn" type="button" onclick="openOverviewEmbyWidgetModal('{instance_id}')" title="Configure Emby" aria-label="Configure Emby">
                <span class="material-icons" aria-hidden="true">settings</span>
              </button>
            </div>
          </div>
          <div class="panel-body">
            <div class="emby-panel-status" data-role="emby-status">Loading Emby…</div>
            <div class="emby-panel-backup-status" data-role="emby-backup-status">Checking backup status…</div>
            <div class="emby-panel-section" data-role="emby-sessions-section">
              <div class="emby-panel-section-title" data-role="emby-sessions-title">Watching Now</div>
              <div class="emby-panel-list" data-role="emby-sessions-list">
                <div class="emby-panel-empty">Checking for active streams…</div>
              </div>
            </div>
            <div class="emby-panel-section">
              <div class="emby-panel-section-title">Recently Added</div>
              <div class="emby-panel-list recent-grid" data-role="emby-latest-list">
                <div class="emby-panel-empty">Loading latest additions…</div>
              </div>
            </div>
          </div>
        </div>
"""
