HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Shiki Dashboard</title>
<link rel="icon" id="app-favicon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2096%2096%22%3E%3Crect%20width%3D%2296%22%20height%3D%2296%22%20fill%3D%22%230a0c0f%22/%3E%3Ctext%20x%3D%2248%22%20y%3D%2258%22%20text-anchor%3D%22middle%22%20font-family%3D%22Inter%2Csans-serif%22%20font-size%3D%2256%22%20font-weight%3D%22700%22%20fill%3D%22%2300e5ff%22%3ES%3C/text%3E%3C/svg%3E"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
:root {
  --bg: #0a0c0f;
  --surface: #111418;
  --surface2: #181c22;
  --border: #1f2530;
  --accent: #00e5ff;
  --accent2: #7b61ff;
  --pass: #00e676;
  --fail: #ff1744;
  --warn: #ffab00;
  --slow: var(--pass);
  --local: #a78bfa;
  --text: #e8eaf0;
  --muted: #5a6278;
  --mono: 'DM Mono', monospace;
  --sans: 'Inter', sans-serif;
  --tab-h: 64px;
  --drive-temp-size: 26px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--sans); min-height: 100vh; }

.layout { display: flex; flex-direction: column; min-height: 100vh; }

.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px; height: 56px; background: var(--surface);
  border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 50; flex-shrink: 0;
}
.topbar-logo { display: flex; align-items: center; gap: 10px; }
.logo-button {
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}
.logo-button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
}
.logo-icon {
  width: 28px; height: 28px; background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 14px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 8px 20px rgba(0,0,0,0.22);
}
.logo-icon.has-image {
  background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
}
.logo-icon img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}
.logo-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bg);
  font-size: 15px;
  font-weight: 700;
}
.topbar-logo h1 { font-size: 16px; font-weight: 700; letter-spacing: -0.3px; }
.topbar-logo h1 span { color: var(--accent); }

.content { flex: 1; overflow-y: auto; padding-bottom: calc(var(--tab-h) + 8px); }

.section { display: none; padding: 20px 16px; }
.section.active { display: block; }

.tab-bar {
  position: fixed; bottom: 0; left: 0; right: 0; height: var(--tab-h);
  background: var(--surface); border-top: 1px solid var(--border);
  display: flex; z-index: 100; padding-bottom: env(safe-area-inset-bottom, 0);
}
.tab-item {
  flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 4px; cursor: pointer; background: none; border: none; color: var(--muted);
  font-family: var(--sans); font-size: 11px; font-weight: 500; padding: 8px 4px 4px;
  transition: color 0.15s; position: relative;
}
.tab-item:hover { color: var(--text); }
.tab-item.active { color: var(--accent); }
.tab-item.active::before {
  content: ''; position: absolute; top: 0; left: 20%; right: 20%; height: 2px;
  background: var(--accent); border-radius: 0 0 2px 2px;
}
.tab-icon {
  font-size: 32px;
  line-height: 1;
  vertical-align: middle;
}
.tab-item .material-icons {
  font-size: 24px;
}
.material-icons {
  font-family: 'Material Icons';
  font-weight: normal;
  font-style: normal;
  font-size: inherit;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  vertical-align: middle;
  white-space: nowrap;
}
.icon-inline {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  margin-right: 4px;
  transform: translateY(-1px);
}
.badge-icon { transform: translateY(-1px); }

.summary-strip { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
@media (min-width: 480px) {
  .summary-strip { grid-template-columns: repeat(4, 1fr); }
  .summary-strip.cols3 { grid-template-columns: repeat(3, 1fr); }
}
.summary-strip.cols2 { grid-template-columns: repeat(2, 1fr); }
.summary-strip.cols3 { grid-template-columns: repeat(3, 1fr); }
.summary-strip.cols4 { grid-template-columns: repeat(4, 1fr); }
.summary-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  padding: 14px 16px; position: relative; overflow: hidden;
}
.summary-card::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; }
.summary-card.total::before { background: var(--accent2); }
.summary-card.healthy::before, .summary-card.up::before { background: var(--pass); }
.summary-card.failing::before, .summary-card.down::before { background: var(--fail); }
.summary-card.temp::before, .summary-card.warn::before { background: var(--warn); }
.summary-card.slow::before { background: var(--slow); }
.summary-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; font-weight: 500; }
.summary-value { font-size: 28px; font-weight: 700; line-height: 1; }
.summary-card.total .summary-value { color: var(--accent2); }
.summary-card.healthy .summary-value, .summary-card.up .summary-value { color: var(--pass); }
.summary-card.failing .summary-value, .summary-card.down .summary-value { color: var(--fail); }
.summary-card.temp .summary-value, .summary-card.warn .summary-value { color: var(--warn); }
.summary-card.slow .summary-value { color: var(--slow); }
.summary-sub { font-size: 11px; color: var(--muted); margin-top: 4px; }

.overview-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
@media (min-width: 700px) { .overview-grid { grid-template-columns: 1fr 1fr; } }
@media (min-width: 1100px) { .overview-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.overview-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; border-bottom: 1px solid var(--border); background: var(--surface2);
}
.panel-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.panel-title { font-size: 13px; font-weight: 600; }
.panel-link {
  font-size: 11px; color: var(--accent); cursor: pointer; background: none; border: none;
  font-family: var(--sans); font-weight: 500;
}
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
.panel-link:hover { text-decoration: underline; }
.panel-body { padding: 12px 16px; }
.overview-drive-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 13px;
}
.overview-drive-row:last-child { border-bottom: none; }
.overview-drive-name { font-weight: 500; }
.overview-drive-meta { color: var(--muted); font-size: 11px; margin-top: 2px; }
.overview-service-row {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 13px;
}
.overview-service-row:last-child { border-bottom: none; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.status-dot.up { background: var(--pass); box-shadow: 0 0 6px var(--pass); }
.status-dot.slow { background: var(--slow); box-shadow: 0 0 6px var(--slow); }
.status-dot.down { background: var(--fail); box-shadow: 0 0 6px var(--fail); animation: pulse-dot 1.5s infinite; }
.status-dot.unknown { background: var(--muted); }
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:0.4} }

.drives-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
@media (min-width: 800px) { .drives-grid { grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); } }
.drive-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  overflow: hidden; transition: border-color 0.2s, transform 0.2s; animation: fadeIn 0.4s ease both;
}
@keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
.drive-card:hover { border-color: var(--accent); }
.drive-card.fail-card { border-color: rgba(255,23,68,0.4); }
.drive-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px; background: var(--surface2); border-bottom: 1px solid var(--border);
}
.drive-title { display: flex; align-items: center; gap: 10px; }
.drive-icon { font-size: 20px; }
.drive-dev { font-family: var(--mono); font-size: 11px; color: var(--muted); margin-top: 2px; }
.health-badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; letter-spacing: 0.5px; }
.health-badge.PASS { background: rgba(0,230,118,0.12); color: var(--pass); border: 1px solid rgba(0,230,118,0.3); }
.health-badge.FAIL { background: rgba(255,23,68,0.12); color: var(--fail); border: 1px solid rgba(255,23,68,0.3); animation: pulse-fail 1.5s infinite; }
.health-badge.UNKNOWN { background: rgba(90,98,120,0.2); color: var(--muted); border: 1px solid var(--border); }
@keyframes pulse-fail { 0%,100%{opacity:1} 50%{opacity:0.6} }
.drive-body { padding: 14px 16px; }
.drive-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.meta-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 500; margin-bottom: 3px; }
.meta-value { font-size: 13px; font-weight: 600; }
.temp-row { display:flex; align-items:center; gap:12px; margin-bottom:14px; padding:10px 12px; background:var(--bg); border-radius:8px; border:1px solid var(--border); }
.temp-number { font-size: var(--drive-temp-size); font-weight: 700; min-width: 66px; }
.temp-cool { color: var(--accent); }
.temp-warm { color: var(--warn); }
.temp-hot  { color: var(--fail); }
.temp-bar-wrap { flex: 1; }
.temp-bar-label { font-size: 10px; color: var(--muted); font-weight: 500; margin-bottom: 5px; }
.temp-bar-track { height: 5px; background: var(--border); border-radius: 3px; overflow: hidden; }
.temp-bar-fill { height: 100%; border-radius: 3px; transition: width 0.8s ease; }
.expand-btn { width:100%; background:none; border:1px solid var(--border); color:var(--muted); padding:7px; border-radius:6px; cursor:pointer; font-family:var(--sans); font-size:12px; font-weight:500; transition:all 0.2s; margin-top:4px; }
.expand-btn:hover { border-color:var(--accent); color:var(--accent); }
.attrs-section { display:none; margin-top:12px; }
.attrs-section.open { display:block; }
.attrs-table { width:100%; border-collapse:collapse; font-family:var(--mono); font-size:11px; }
.attrs-table th { text-align:left; padding:5px 8px; color:var(--muted); font-weight:400; border-bottom:1px solid var(--border); text-transform:uppercase; letter-spacing:0.5px; }
.attrs-table td { padding:5px 8px; border-bottom:1px solid rgba(31,37,48,0.6); }
.attrs-table tr:last-child td { border-bottom:none; }
.attrs-table tr.attr-failed td { color:var(--fail); background:rgba(255,23,68,0.05); }
.attr-raw { color:var(--muted); }
.history-section { margin-top:12px; display:none; }
.history-section.open { display:block; }
.chart-wrap { background:var(--bg); border:1px solid var(--border); border-radius:8px; padding:12px; }
.chart-title { font-size:10px; color:var(--muted); font-family:var(--mono); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
canvas { display:block; width:100% !important; }

.drive-nickname { font-size: 14px; font-weight: 600; color: var(--text); }
.rename-btn { background:none; border:none; color:var(--muted); cursor:pointer; font-size:12px; padding:2px 4px; border-radius:4px; transition:color 0.2s; }
.rename-btn:hover { color:var(--accent); }
.rename-input-row { display:none; align-items:center; gap:6px; margin-top:4px; }
.rename-input-row.open { display:flex; }
.rename-input { background:var(--bg); border:1px solid var(--accent); color:var(--text); padding:4px 8px; border-radius:5px; font-family:var(--sans); font-size:13px; outline:none; width:140px; }
.rename-save { background:var(--accent); border:none; color:var(--bg); padding:4px 10px; border-radius:5px; font-family:var(--sans); font-size:12px; font-weight:600; cursor:pointer; }
.rename-cancel { background:none; border:1px solid var(--border); color:var(--muted); padding:4px 10px; border-radius:5px; font-family:var(--sans); font-size:12px; cursor:pointer; }

/* ---- Services ---- */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}
.debrid-header {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: nowrap;
  width: 100%;
  margin-bottom: 6px;
}
.debrid-header > :first-child {
  flex: 0 1 auto;
  min-width: 0;
}
.section-header .section-title {
  font-size: 14px;
  font-weight: 600;
}
.section-header .section-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}
.debrid-magnet-area {
  flex: 1 1 auto;
  min-width: 0;
  display: flex;
  align-items: center;
}
.debrid-magnet-input {
  width: 100%;
  min-width: 0;
  font-size: 13px;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text);
}
.debrid-header .section-actions {
  flex: 0 0 auto;
}
.debrid-magnet-input:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.debrid-magnet-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}
.debrid-magnet-status {
  font-size: 12px;
  color: var(--muted);
  margin: -4px 52px 2px auto;
  width: min(100%, 640px);
}
.debrid-magnet-status:empty {
  display: none;
}
.debrid-magnet-status.success {
  color: var(--pass);
}
.debrid-magnet-status.error {
  color: var(--fail);
}
@media (max-width: 900px) {
  .debrid-magnet-status {
    margin: -4px 0 2px 0;
    width: 100%;
  }
}
.section-subtitle {
  font-size: 13px;
  color: var(--muted);
}
.section-subtitle.small-muted {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}
.debrid-queue-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.debrid-queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--muted);
}
.debrid-queue-status {
  font-family: var(--mono);
  font-size: 13px;
  color: var(--text);
  min-height: 20px;
}
.debrid-queue-body {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--accent);
  background: rgba(0, 0, 0, 0.15);
  border-radius: 6px;
  padding: 8px;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 160px;
  overflow: auto;
}
.debrid-queue-wrapper {
  margin-top: 12px;
}
.debrid-queue-wrapper.hidden {
  display: none;
}
.debrid-queue-list {
  margin-top: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.debrid-queue-item {
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.debrid-queue-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-family: var(--sans);
}
.debrid-queue-item-name {
  flex: 1 1 auto;
  min-width: 0;
  font-weight: 600;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.debrid-queue-item-meta {
  display: flex;
  flex-direction: column;
  flex: 0 0 auto;
  gap: 4px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--muted);
  align-items: flex-end;
}
.debrid-queue-item-meta-row {
  display: flex;
  gap: 8px;
  flex-wrap: nowrap;
  white-space: nowrap;
}
.debrid-progress {
  height: 8px;
  background: var(--border);
  border-radius: 999px;
  overflow: hidden;
}
.debrid-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border-radius: inherit;
  transition: width 0.35s ease;
}
.debrid-queue-empty {
  font-size: 13px;
  color: var(--muted);
  font-family: var(--sans);
}
.icon-btn {
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text);
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s, background 0.2s;
}
.icon-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}
.icon-btn.spinning {
  border-color: var(--accent);
  color: var(--accent);
  cursor: default;
  pointer-events: none;
}
.icon-btn.spinning .material-icons {
  animation: spin 0.8s linear infinite;
}
.add-service-btn {
  background: var(--accent); color: var(--bg); border: none; padding: 8px 16px; border-radius: 7px;
  font-family: var(--sans); font-size: 13px; font-weight: 600; cursor: pointer; transition: opacity 0.2s;
}
.add-service-btn:hover { opacity: 0.85; }
.services-grid { display: grid; grid-template-columns: 1fr; gap: 14px; }
@media (min-width: 700px) { .services-grid { grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); } }
.service-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  overflow: hidden; animation: fadeIn 0.3s ease both;
}
.service-card.svc-down { border-color: rgba(255,23,68,0.35); }
.service-card.svc-slow { border-color: rgba(0,230,118,0.25); }
.service-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 14px; background: var(--surface2); border-bottom: 1px solid var(--border);
}
.service-title-row { display: flex; align-items: center; gap: 10px; }
.service-name { font-size: 14px; font-weight: 600; }
.service-title-clickable { transition: color 0.2s; }
.service-title-clickable:hover { color: #b8c1d0; }
.service-url { font-family: var(--mono); font-size: 11px; color: var(--muted); margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 200px; }
.svc-badges { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; justify-content: flex-end; }
.svc-expansion-footer { display: flex; justify-content: flex-end; padding-top: 10px; margin-top: 8px; border-top: 1px solid rgba(31,37,48,0.5); }
.svc-history-toggle { background: none; border: none; color: var(--muted); cursor: pointer; font-size: 14px; padding: 4px 6px; line-height: 1; transition: color 0.2s, transform 0.3s; }
.svc-history-toggle:hover { color: var(--accent); }
.svc-history-toggle.rotated { transform: rotate(180deg); }
.svc-badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.svc-badge.up { background: rgba(0,230,118,0.12); color: var(--pass); border: 1px solid rgba(0,230,118,0.3); }
.svc-badge.slow { background: rgba(0,230,118,0.12); color: var(--pass); border: 1px solid rgba(0,230,118,0.3); }
.svc-badge.down { background: rgba(255,23,68,0.12); color: var(--fail); border: 1px solid rgba(255,23,68,0.3); animation: pulse-fail 1.5s infinite; }
.svc-badge.unknown { background: rgba(90,98,120,0.15); color: var(--muted); border: 1px solid var(--border); }
.svc-badge.local-badge.up { background: rgba(0,230,118,0.12); color: var(--pass); border: 1px solid rgba(0,230,118,0.3); }
.svc-badge.local-badge.slow { background: rgba(0,230,118,0.12); color: var(--pass); border: 1px solid rgba(0,230,118,0.3); }
.svc-badge.local-badge.down { background: rgba(255,23,68,0.12); color: var(--fail); border: 1px solid rgba(255,23,68,0.3); animation: pulse-fail 1.5s infinite; }
.svc-badge.local-badge.unknown { background: rgba(90,98,120,0.15); color: var(--muted); border: 1px solid var(--border); }
.service-body { padding: 12px 14px; }
.service-meta-row { display: flex; gap: 16px; margin-bottom: 12px; flex-wrap: wrap; }
.svc-meta-item .meta-label { font-size: 10px; }
.svc-meta-item .meta-value { font-size: 13px; font-weight: 600; }

.bar-row { display: flex; flex-direction: column; gap: 3px; }
.bar-row-label {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 10px; color: var(--muted); font-family: var(--mono);
}
.bar-row-label-left {
  display: flex; align-items: center; gap: 8px;
}
.bar-row-label-left span {
  font-size: 13px; color: var(--text); font-family: var(--mono);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.svc-link {
  color: var(--accent); cursor: pointer; text-decoration: underline;
}
.svc-link:hover {
  color: #8eefff;
}
.bar-tag {
  display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 9px;
  font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;
}
.bar-tag.ext { background: rgba(0,229,255,0.1); color: var(--accent); border: 1px solid rgba(0,229,255,0.2); }
.bar-tag.loc { background: rgba(167,139,250,0.12); color: var(--local); border: 1px solid rgba(167,139,250,0.25); }

/* History bars */
.history-bar { display: flex; gap: 2px; align-items: flex-end; }
.hb-dot { flex: 1; height: 20px; border-radius: 2px; background: var(--border); transition: background 0.2s; cursor: default; position: relative; }
.hb-dot.up { background: var(--pass); opacity: 0.7; }
.hb-dot.up:hover { opacity: 1; }
.hb-dot.slow { background: var(--slow); opacity: 0.8; }
.hb-dot.slow:hover { opacity: 1; }
.hb-dot.down { background: var(--fail); opacity: 0.9; }
.hb-dot.unknown { background: var(--border); }
/* Local bar uses same green/yellow/red scheme as external */

.svc-actions { display: flex; gap: 6px; margin-top: 4px; flex-wrap: wrap; }
.svc-btn { background:none; border:1px solid var(--border); color:var(--muted); padding:5px 10px; border-radius:5px; font-family:var(--sans); font-size:11px; font-weight:500; cursor:pointer; transition:all 0.2s; }
.svc-btn:hover { border-color:var(--accent); color:var(--accent); }
.svc-btn.danger:hover { border-color:var(--fail); color:var(--fail); }

/* Service data groups */
.service-data-groups {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 10px;
}
.service-data-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.chart-wrap.hidden {
  display: none;
}

/* Local section divider in modal */
.modal-divider { border: none; border-top: 1px solid var(--border); margin: 16px 0 14px; }
.modal-section-label { font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.modal-section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.local-optional { font-size: 10px; color: var(--muted); font-weight: 400; text-transform: none; letter-spacing: 0; margin-left: 4px; }

.modal-overlay {
  display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 200;
  align-items: flex-end; justify-content: center; padding: 0;
}
@media (min-width: 500px) { .modal-overlay { align-items: center; padding: 16px; } }
.modal-overlay.open { display: flex; }
.modal {
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px 14px 0 0;
  padding: 24px 20px; width: 100%; max-width: 460px; max-height: 90vh; overflow-y: auto;
}
@media (min-width: 500px) { .modal { border-radius: 14px; } }
.modal.reorder-modal { max-width: 520px; }
.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}
.modal-header h2 { margin: 0 0 4px; font-size: 18px; }
.modal-subtitle {
  font-size: 12px;
  color: var(--muted);
  max-width: 320px;
}
.modal-close-btn {
  min-width: 36px;
  min-height: 36px;
  padding: 0;
}
.modal h2 { font-size: 16px; font-weight: 700; margin-bottom: 18px; }
.form-group { margin-bottom: 14px; }
.form-label { font-size: 11px; font-weight: 500; color: var(--muted); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px; display: block; }
.form-input, .form-select {
  width: 100%; background: var(--bg); border: 1px solid var(--border); color: var(--text);
  padding: 9px 12px; border-radius: 7px; font-family: var(--sans); font-size: 14px; outline: none; transition: border-color 0.2s;
}
.form-input:focus, .form-select:focus { border-color: var(--accent); }
.form-select option { background: var(--bg); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; align-items: center; }
.modal-delete-btn { color: var(--fail); border-color: var(--fail); }
.modal-delete-btn:hover { background: rgba(255,23,68,0.1); }
.btn-primary { background: var(--accent); color: var(--bg); border: none; padding: 9px 20px; border-radius: 7px; font-family: var(--sans); font-size: 14px; font-weight: 600; cursor: pointer; min-height: 44px; }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; }
.btn-secondary { background: none; color: var(--muted); border: 1px solid var(--border); padding: 9px 20px; border-radius: 7px; font-family: var(--sans); font-size: 14px; cursor: pointer; min-height: 44px; }

.logo-modal {
  max-width: 720px;
}
.logo-upload-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.logo-upload-help {
  font-size: 12px;
  color: var(--muted);
}
.logo-editor-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 18px;
}
@media (min-width: 720px) {
  .logo-editor-grid {
    grid-template-columns: minmax(0, 1.6fr) minmax(220px, 0.9fr);
    align-items: start;
  }
}
.logo-crop-stage {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 12px;
}
.logo-crop-canvas {
  width: 100%;
  display: block;
  border-radius: 10px;
  background:
    linear-gradient(45deg, rgba(255,255,255,0.04) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.04) 75%),
    linear-gradient(45deg, rgba(255,255,255,0.04) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.04) 75%);
  background-position: 0 0, 12px 12px;
  background-size: 24px 24px;
  touch-action: none;
  cursor: grab;
}
.logo-crop-canvas.dragging {
  cursor: grabbing;
}
.logo-editor-panel {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
}
.logo-preview-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}
.logo-preview {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  flex-shrink: 0;
}
.logo-preview img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}
.logo-preview-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.logo-preview-label {
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}
.logo-preview-title {
  font-size: 14px;
  font-weight: 600;
}
.logo-controls {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.logo-range-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 6px;
}
.logo-range {
  width: 100%;
  height: 4px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  touch-action: none;
  cursor: pointer;
}
.logo-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid rgba(0, 0, 0, 0.25);
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.35);
  margin-top: -6px;
}
.logo-range::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid rgba(0, 0, 0, 0.25);
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.35);
}
.logo-range::-webkit-slider-runnable-track {
  height: 4px;
}
.logo-action-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.logo-empty {
  background: var(--bg);
  border: 1px dashed var(--border);
  color: var(--muted);
  border-radius: 14px;
  padding: 28px 18px;
  text-align: center;
  font-size: 13px;
}

.reorder-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 360px;
  overflow-y: auto;
}
.reorder-item {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.reorder-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  flex: 1;
}
.reorder-meta {
  font-size: 11px;
  color: var(--muted);
  margin-top: 2px;
}
.reorder-controls {
  display: flex;
  gap: 6px;
}
.reorder-controls button {
  border: 1px solid var(--border);
  background: transparent;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--text);
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
}
.reorder-controls button:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}
.reorder-controls button:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.loading { text-align:center; padding:50px 20px; color:var(--muted); }
.loading-spinner { width:32px; height:32px; border:2px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin 0.8s linear infinite; margin:0 auto 12px; }
@keyframes spin { to{transform:rotate(360deg)} }
.empty-state { text-align: center; padding: 50px 20px; color: var(--muted); }
.empty-state .empty-icon { font-size: 36px; margin-bottom: 10px; }
.empty-state p { font-size: 14px; }
</style>
</head>
<body>
<div class="layout">

  <div class="topbar">
    <div class="topbar-logo">
      <button class="logo-button" type="button" onclick="openLogoModal()" aria-label="Edit app logo" title="Edit app logo">
        <div class="logo-icon" id="app-logo-button">
          <div class="logo-fallback">S</div>
        </div>
      </button>
      <h1>Shiki<span>Dashboard</span></h1>
    </div>
  </div>

  <div class="content">

    <div class="section active" id="section-overview">
      <div class="overview-grid">
        <div class="overview-panel host-panel">
          <div class="panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">monitor_heart</span>
              <span class="panel-title">Host Resource Statistics</span>
            </div>
          </div>
          <div class="panel-body">
            <div class="host-stats-list">
              <div class="host-stat-row">
                <div class="host-stat-label">CPU</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" id="host-stat-cpu-value">—</div>
                  <div class="host-stat-sub" id="host-stat-cpu-sub">—</div>
                </div>
              </div>
              <div class="host-stat-row">
                <div class="host-stat-label">RAM</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" id="host-stat-ram-value">—</div>
                  <div class="host-stat-sub" id="host-stat-ram-sub">—</div>
                </div>
              </div>
              <div class="host-stat-row">
                <div class="host-stat-label">Upload</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" id="host-stat-upload-value">—</div>
                  <div class="host-stat-sub" id="host-stat-upload-sub">—</div>
                </div>
              </div>
              <div class="host-stat-row">
                <div class="host-stat-label">Download</div>
                <div class="host-stat-value-group">
                  <div class="host-stat-value" id="host-stat-download-value">—</div>
                  <div class="host-stat-sub" id="host-stat-download-sub">—</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="overview-panel">
          <div class="panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">public</span>
              <span class="panel-title">Service Status</span>
            </div>
            <button class="panel-link" onclick="navigate('services')">View all →</button>
          </div>
          <div class="panel-body" id="ov-services-list">
            <div class="loading"><div class="loading-spinner"></div></div>
          </div>
        </div>
        <div class="overview-panel">
          <div class="panel-header">
            <div class="panel-title-group">
              <span class="material-icons icon-inline">storage</span>
              <span class="panel-title">Drive Status</span>
            </div>
            <button class="panel-link" onclick="navigate('disks')">View all →</button>
          </div>
          <div class="panel-body" id="ov-drives-list">
            <div class="loading"><div class="loading-spinner"></div></div>
          </div>
        </div>
      </div>
    </div>

    <div class="section" id="section-disks">
      <div class="summary-strip">
        <div class="summary-card total">
          <div class="summary-label">Total</div>
          <div class="summary-value" id="s-total">—</div>
        </div>
        <div class="summary-card healthy">
          <div class="summary-label">Healthy</div>
          <div class="summary-value" id="s-healthy">—</div>
        </div>
        <div class="summary-card failing">
          <div class="summary-label">Failing</div>
          <div class="summary-value" id="s-failing">—</div>
        </div>
        <div class="summary-card temp">
          <div class="summary-label">Avg Temp</div>
          <div class="summary-value" id="s-temp">—</div>
        </div>
      </div>
      <div class="section-header">
        <div>
          <div class="section-title">Disks</div>
          <div class="section-subtitle small-muted" id="disks-updated-text">Never scanned</div>
        </div>
        <div class="section-actions">
          <button class="icon-btn" id="disks-refresh-btn" type="button" title="Refresh drives" aria-label="Refresh drives" onclick="refreshCurrent(true)">
            <span class="material-icons">refresh</span>
          </button>
          <button class="icon-btn" type="button" title="Reorder drives" onclick="openReorderModal('drives')">
            <span class="material-icons">settings</span>
          </button>
        </div>
      </div>
      <div id="drives-container">
        <div class="loading"><div class="loading-spinner"></div>Scanning drives…</div>
      </div>
    </div>

    <div class="section" id="section-services">
      <div class="summary-strip cols2">
        <div class="summary-card up">
          <div class="summary-label">Online</div>
          <div class="summary-value" id="ss-up">—</div>
        </div>
        <div class="summary-card down">
          <div class="summary-label">Offline</div>
          <div class="summary-value" id="ss-down">—</div>
        </div>
      </div>
      <div class="section-header">
        <div>
          <div class="section-title">Services</div>
        </div>
        <div class="section-actions">
          <button class="icon-btn" type="button" title="Add Service" aria-label="Add Service" onclick="openAddModal()">
            <span class="material-icons">add</span>
          </button>
          <button class="icon-btn" type="button" id="services-history-btn" title="Show service history" aria-label="Show service history" onclick="toggleServiceHistoryVisibility()">
            <span class="material-icons" id="services-history-icon">expand_more</span>
          </button>
          <button class="icon-btn" type="button" title="Reorder services" onclick="openReorderModal('services')">
            <span class="material-icons">settings</span>
          </button>
        </div>
      </div>
      <div id="services-container">
        <div class="loading"><div class="loading-spinner"></div>Loading…</div>
      </div>
    </div>

    <div class="section" id="section-debrid">
      <div class="section-header debrid-header">
        <div>
          <div class="section-title">Debrid Client</div>
          <div class="section-subtitle small-muted" id="debrid-status">Not configured</div>
        </div>
        <div class="debrid-magnet-area">
          <input autocomplete="off" class="form-input debrid-magnet-input" id="debrid-magnet-input" type="text" placeholder="Magnet Link"/>
        </div>
        <div class="section-actions">
          <button class="icon-btn" type="button" id="debrid-queue-toggle-btn" title="Hide queue panel" aria-label="Hide queue panel" onclick="toggleDebridQueueVisibility()">
            <span class="material-icons" id="debrid-queue-toggle-icon">expand_less</span>
          </button>
          <button class="icon-btn" type="button" title="Configure Debrid Client" aria-label="Configure Debrid Client" onclick="openDebridModal()">
            <span class="material-icons">settings</span>
          </button>
        </div>
      </div>
      <div class="debrid-magnet-status" id="debrid-magnet-status" aria-live="polite"></div>
      <div class="debrid-queue-list" id="debrid-queue-list">
        <div class="debrid-queue-empty">Queue data will populate once the proxy succeeds.</div>
      </div>
      <div class="debrid-queue-wrapper" id="debrid-queue-wrapper">
        <div class="debrid-queue-card">
          <div class="debrid-queue-header">
            <span>Queue probe</span>
            <span id="debrid-queue-time">—</span>
          </div>
          <div class="debrid-queue-status" id="debrid-queue-status">Waiting for configuration…</div>
          <pre class="debrid-queue-body" id="debrid-queue-body">Response body appears here.</pre>
        </div>
      </div>
    </div>

  </div>

  <nav class="tab-bar">
    <button class="tab-item active" id="tab-overview" onclick="navigate('overview')">
      <span class="tab-icon material-icons">home</span><span>Overview</span>
    </button>
    <button class="tab-item" id="tab-services" onclick="navigate('services')">
      <span class="tab-icon material-icons">public</span><span>Services</span>
    </button>
    <button class="tab-item" id="tab-disks" onclick="navigate('disks')">
      <span class="tab-icon material-icons">storage</span><span>Disks</span>
    </button>
    <button class="tab-item" id="tab-debrid" onclick="navigate('debrid')">
      <span class="tab-icon material-icons">cloud</span><span>Debrid</span>
    </button>
  </nav>

</div>

<!-- Add/Edit Service Modal -->
<div class="modal-overlay" id="add-modal">
  <div class="modal">
    <h2 id="modal-title">Add Service Monitor</h2>

    <div class="form-group">
      <label class="form-label">Service Name</label>
      <input class="form-input" id="svc-name" type="text" placeholder="e.g. Plex, Router, NAS"/>
    </div>

    <div class="modal-section-label">LOCAL SERVICE INFO</div>
    <div class="form-group">
      <label class="form-label">Local IP / Host</label>
      <input class="form-input" id="svc-local-url" type="text" placeholder="e.g. 192.168.1.10:32400"/>
    </div>
    <div class="form-group" style="max-width:160px">
      <label class="form-label">Check Type</label>
      <select class="form-select" id="svc-local-type">
        <option value="tcp">TCP Port</option>
        <option value="ping">Ping</option>
        <option value="http">HTTP/HTTPS</option>
      </select>
    </div>

    <hr class="modal-divider"/>
    <div class="modal-section-label">EXTERNAL SERVICE INFO <span class="local-optional">(optional)</span></div>
    <div class="form-group">
      <label class="form-label">URL / Host</label>
      <input class="form-input" id="svc-url" type="text" placeholder="e.g. https://plex.yourdomain.com"/>
    </div>
    <div class="form-row-3">
      <div class="form-group">
        <label class="form-label">Check Type</label>
        <select class="form-select" id="svc-type">
          <option value="http">HTTP/HTTPS</option>
          <option value="ping">Ping</option>
          <option value="tcp">TCP Port</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Interval (sec)</label>
        <input class="form-input" id="svc-interval" type="number" value="60" min="10"/>
      </div>
      <div class="form-group">
        <label class="form-label">Graph Window</label>
        <select class="form-select" id="svc-chart-window">
          <option value="300">5 min</option>
          <option value="1800">30 min</option>
          <option value="2700" selected>45 min</option>
          <option value="3600">1 hour</option>
          <option value="10800">3 hours</option>
          <option value="43200">12 hours</option>
          <option value="86400">24 hours</option>
        </select>
      </div>
    </div>

    <div class="modal-actions">
      <button class="btn-secondary modal-delete-btn" id="modal-delete-btn" onclick="deleteServiceFromModal()" style="display:none" title="Remove service"><span class="material-icons">delete</span></button>
      <div style="flex:1"></div>
      <button class="btn-secondary" onclick="closeAddModal()">Cancel</button>
      <button class="btn-primary" id="modal-submit-btn" onclick="submitAddService()">Add Service</button>
    </div>
  </div>
</div>

<div class="modal-overlay" id="reorder-modal">
  <div class="modal reorder-modal">
    <div class="modal-header">
      <div>
        <h2 id="reorder-modal-title">Reorder items</h2>
        <div class="modal-subtitle" id="reorder-modal-subtitle">Adjust the display order and save to persist the layout.</div>
      </div>
      <button class="icon-btn modal-close-btn" type="button" onclick="closeReorderModal()" title="Close">
        <span class="material-icons">close</span>
      </button>
    </div>
    <ul class="reorder-list" id="reorder-list"></ul>
    <div class="modal-actions">
      <button class="btn-secondary" type="button" onclick="closeReorderModal()">Cancel</button>
      <button class="btn-primary" type="button" onclick="saveReorderChanges()">Save Order</button>
    </div>
  </div>
</div>

<div class="modal-overlay" id="logo-modal">
  <div class="modal logo-modal">
    <div class="modal-header">
      <div>
        <h2>App Logo</h2>
        <div class="modal-subtitle">Upload an image, drag the square crop, and save. Reopening this editor restores the original image and your last crop.</div>
      </div>
      <button class="icon-btn modal-close-btn" type="button" onclick="closeLogoModal()" title="Close">
        <span class="material-icons">close</span>
      </button>
    </div>

    <div class="logo-upload-row">
      <input id="logo-file-input" type="file" accept="image/*" onchange="handleLogoFileInput(event)"/>
      <div class="logo-upload-help">Square crops work best with larger images. PNG, JPG, and WebP are all fine.</div>
    </div>

    <div id="logo-editor-content">
      <div class="logo-empty">Upload a logo to replace the current app icon.</div>
    </div>

    <div class="modal-actions">
      <button class="btn-secondary" type="button" onclick="closeLogoModal()">Cancel</button>
      <button class="btn-primary" type="button" id="logo-save-btn" onclick="saveLogoConfig()" disabled>Save Logo</button>
    </div>
  </div>
</div>

<div class="modal-overlay" id="debrid-modal">
  <div class="modal">
    <div class="modal-header">
      <div>
        <h2>Debrid Client</h2>
        <div class="modal-subtitle">Store the Real Debrid Client connection details used by this dashboard.</div>
      </div>
      <button class="icon-btn modal-close-btn" type="button" onclick="closeDebridModal()" title="Close">
        <span class="material-icons">close</span>
      </button>
    </div>

    <div class="form-group">
      <label class="form-label">Real Debrid Client IP</label>
      <input class="form-input" id="debrid-ip-input" type="text" placeholder="e.g. 192.168.1.42"/>
    </div>
    <div class="form-group">
      <label class="form-label">Username</label>
      <input class="form-input" id="debrid-username-input" type="text"/>
    </div>
    <div class="form-group">
      <label class="form-label">Password</label>
      <input class="form-input" id="debrid-password-input" type="password"/>
    </div>

    <div class="modal-actions">
      <button class="btn-secondary" type="button" onclick="closeDebridModal()">Cancel</button>
      <button class="btn-primary" type="button" id="debrid-save-btn" onclick="submitDebridConfig()">Save</button>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script>
let currentSection = 'overview';
const charts = {};
let nicknames = {};
let drivesCache = [];
let servicesCache = [];
let hostStatsTimer = null;
let svcHistoryVisible = false;
let debridQueueVisible = true;
let logoConfig = { original_image: null, crop: null };
let logoEditorImage = null;
let logoEditorCanvas = null;
let logoEditorCtx = null;
let logoEditorScale = 1;
let logoDragState = null;
let logoRenderQueued = false;
let debridConfig = { ip: '', username: '', password: '', updated_at: null };
let debridQueueTimer = null;
let magnetSubmissionInProgress = false;
let magnetStatusTimer = null;

const DEFAULT_FAVICON_DATA_URL = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2096%2096%22%3E%3Crect%20width%3D%2296%22%20height%3D%2296%22%20fill%3D%22%230a0c0f%22/%3E%3Ctext%20x%3D%2248%22%20y%3D%2258%22%20text-anchor%3D%22middle%22%20font-family%3D%22Inter%2Csans-serif%22%20font-size%3D%2256%22%20font-weight%3D%22700%22%20fill%3D%22%2300e5ff%22%3ES%3C/text%3E%3C/svg%3E";

function updateFavicon(dataUrl) {
  const link = document.getElementById('app-favicon');
  if (!link) return;
  link.href = dataUrl || DEFAULT_FAVICON_DATA_URL;
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function defaultLogoCrop(width, height) {
  const size = Math.min(width, height);
  return {
    x: Math.round((width - size) / 2),
    y: Math.round((height - size) / 2),
    size,
  };
}

function sanitizeLogoCrop(crop, width, height) {
  if (!crop || !Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
    return defaultLogoCrop(width, height);
  }
  let size = Number(crop.size);
  if (!Number.isFinite(size) || size <= 0) size = Math.min(width, height);
  size = clamp(size, 32, Math.min(width, height));
  let x = Number(crop.x);
  let y = Number(crop.y);
  if (!Number.isFinite(x)) x = 0;
  if (!Number.isFinite(y)) y = 0;
  x = clamp(x, 0, Math.max(0, width - size));
  y = clamp(y, 0, Math.max(0, height - size));
  return {
    x: Math.round(x),
    y: Math.round(y),
    size: Math.round(size),
  };
}

function getLogoCropPercent() {
  if (!logoEditorImage || !logoConfig.crop) return 100;
  return Math.round((logoConfig.crop.size / Math.min(logoEditorImage.naturalWidth, logoEditorImage.naturalHeight)) * 100);
}

function setLogoCropPercent(percent) {
  if (!logoEditorImage) return;
  const width = logoEditorImage.naturalWidth;
  const height = logoEditorImage.naturalHeight;
  const maxSize = Math.min(width, height);
  const nextSize = clamp(Math.round((clamp(percent, 5, 100) / 100) * maxSize), 32, maxSize);
  const crop = sanitizeLogoCrop({
    x: logoConfig.crop?.x ?? 0,
    y: logoConfig.crop?.y ?? 0,
    size: nextSize,
  }, width, height);
  logoConfig.crop = crop;
}

function queueLogoRender() {
  if (logoRenderQueued) return;
  logoRenderQueued = true;
  requestAnimationFrame(() => {
    logoRenderQueued = false;
    renderLogoEditorCanvas();
  });
}

function getLogoCanvasMetrics() {
  if (!logoEditorCanvas || !logoEditorImage) return null;
  const width = logoEditorCanvas.width;
  const height = logoEditorCanvas.height;
  const imageWidth = logoEditorImage.naturalWidth;
  const imageHeight = logoEditorImage.naturalHeight;
  const scale = Math.min(width / imageWidth, height / imageHeight);
  const drawWidth = imageWidth * scale;
  const drawHeight = imageHeight * scale;
  const offsetX = (width - drawWidth) / 2;
  const offsetY = (height - drawHeight) / 2;
  return { width, height, imageWidth, imageHeight, scale, drawWidth, drawHeight, offsetX, offsetY };
}

function renderLogoEditorCanvas() {
  if (!logoEditorCanvas || !logoEditorCtx || !logoEditorImage || !logoConfig.crop) return;
  const metrics = getLogoCanvasMetrics();
  if (!metrics) return;
  const { width, height, scale, drawWidth, drawHeight, offsetX, offsetY } = metrics;
  logoEditorScale = scale;
  logoEditorCtx.clearRect(0, 0, width, height);
  logoEditorCtx.drawImage(logoEditorImage, offsetX, offsetY, drawWidth, drawHeight);

  const crop = logoConfig.crop;
  const cropX = offsetX + crop.x * scale;
  const cropY = offsetY + crop.y * scale;
  const cropSize = crop.size * scale;

  logoEditorCtx.save();
  logoEditorCtx.fillStyle = 'rgba(0, 0, 0, 0.55)';
  logoEditorCtx.fillRect(0, 0, width, height);
  logoEditorCtx.clearRect(cropX, cropY, cropSize, cropSize);
  logoEditorCtx.drawImage(
    logoEditorImage,
    crop.x, crop.y, crop.size, crop.size,
    cropX, cropY, cropSize, cropSize
  );
  logoEditorCtx.strokeStyle = '#00e5ff';
  logoEditorCtx.lineWidth = 2;
  logoEditorCtx.strokeRect(cropX, cropY, cropSize, cropSize);
  logoEditorCtx.setLineDash([5, 5]);
  logoEditorCtx.strokeStyle = 'rgba(255,255,255,0.45)';
  logoEditorCtx.strokeRect(cropX + cropSize / 3, cropY, 0, cropSize);
  logoEditorCtx.strokeRect(cropX + (cropSize * 2) / 3, cropY, 0, cropSize);
  logoEditorCtx.strokeRect(cropX, cropY + cropSize / 3, cropSize, 0);
  logoEditorCtx.strokeRect(cropX, cropY + (cropSize * 2) / 3, cropSize, 0);
  logoEditorCtx.restore();
}

function renderLogoPreview() {
  const preview = document.getElementById('logo-preview');
  if (!preview) return;
  const dataUrl = getCroppedLogoDataUrl(192);
  if (dataUrl) {
    preview.innerHTML = `<img src="${dataUrl}" alt="Logo preview"/>`;
  } else {
    preview.innerHTML = '<div class="logo-fallback">S</div>';
  }
}

function renderLogoButton() {
  const button = document.getElementById('app-logo-button');
  if (!button) return;
  const dataUrl = getCroppedLogoDataUrl(96);
  if (dataUrl) {
    button.classList.add('has-image');
    button.innerHTML = `<img src="${dataUrl}" alt="App logo"/>`;
  } else {
    button.classList.remove('has-image');
    button.innerHTML = '<div class="logo-fallback">S</div>';
  }
  updateFavicon(dataUrl);
}

function renderLogoEditor() {
  const container = document.getElementById('logo-editor-content');
  const saveBtn = document.getElementById('logo-save-btn');
  if (!container || !saveBtn) return;

  if (!logoConfig.original_image || !logoEditorImage || !logoConfig.crop) {
    container.innerHTML = '<div class="logo-empty">Upload a logo to replace the current app icon.</div>';
    saveBtn.disabled = true;
    return;
  }

  const cropPercent = getLogoCropPercent();
  container.innerHTML = `
    <div class="logo-editor-grid">
      <div class="logo-crop-stage">
        <canvas class="logo-crop-canvas" id="logo-crop-canvas" width="520" height="360"></canvas>
      </div>
      <div class="logo-editor-panel">
        <div class="logo-preview-wrap">
          <div class="logo-preview" id="logo-preview"></div>
          <div class="logo-preview-meta">
            <div class="logo-preview-label">Preview</div>
            <div class="logo-preview-title">Top-left app icon</div>
            <div class="logo-upload-help">${logoEditorImage.naturalWidth} × ${logoEditorImage.naturalHeight}px original</div>
          </div>
        </div>
        <div class="logo-controls">
          <div>
            <div class="logo-range-label">
              <span>Crop size</span>
              <span id="logo-crop-size-label">${cropPercent}%</span>
            </div>
            <input class="logo-range" id="logo-crop-size" type="range" min="5" max="100" step="1" value="${cropPercent}" oninput="handleLogoCropSizeInput(event)"/>
          </div>
          <div class="logo-action-row">
            <button class="btn-secondary" type="button" onclick="centerLogoCrop()">Center crop</button>
            <button class="btn-secondary" type="button" onclick="triggerLogoFilePicker()">Replace image</button>
          </div>
          <div class="logo-upload-help">Drag the highlighted square on the image to move the crop. Use the slider to make the square larger or smaller.</div>
        </div>
      </div>
    </div>
  `;
  saveBtn.disabled = false;

  logoEditorCanvas = document.getElementById('logo-crop-canvas');
  logoEditorCtx = logoEditorCanvas.getContext('2d');
  attachLogoCanvasHandlers();
  renderLogoPreview();
  queueLogoRender();
}

function attachLogoCanvasHandlers() {
  if (!logoEditorCanvas) return;
  logoEditorCanvas.addEventListener('pointerdown', onLogoCanvasPointerDown);
  logoEditorCanvas.addEventListener('pointermove', onLogoCanvasPointerMove);
  logoEditorCanvas.addEventListener('pointerup', onLogoCanvasPointerUp);
  logoEditorCanvas.addEventListener('pointerleave', onLogoCanvasPointerUp);
  logoEditorCanvas.addEventListener('pointercancel', onLogoCanvasPointerUp);
}

function canvasPointToImagePoint(event) {
  if (!logoEditorCanvas) return null;
  const rect = logoEditorCanvas.getBoundingClientRect();
  const scaleX = logoEditorCanvas.width / rect.width;
  const scaleY = logoEditorCanvas.height / rect.height;
  return {
    x: (event.clientX - rect.left) * scaleX,
    y: (event.clientY - rect.top) * scaleY,
  };
}

function onLogoCanvasPointerDown(event) {
  if (!logoConfig.crop || !logoEditorImage) return;
  const point = canvasPointToImagePoint(event);
  const metrics = getLogoCanvasMetrics();
  if (!point || !metrics) return;
  const cropX = metrics.offsetX + logoConfig.crop.x * metrics.scale;
  const cropY = metrics.offsetY + logoConfig.crop.y * metrics.scale;
  const cropSize = logoConfig.crop.size * metrics.scale;
  if (point.x < cropX || point.x > cropX + cropSize || point.y < cropY || point.y > cropY + cropSize) return;
  logoDragState = {
    pointerId: event.pointerId,
    startX: point.x,
    startY: point.y,
    cropX: logoConfig.crop.x,
    cropY: logoConfig.crop.y,
  };
  logoEditorCanvas.classList.add('dragging');
  logoEditorCanvas.setPointerCapture(event.pointerId);
}

function onLogoCanvasPointerMove(event) {
  if (!logoDragState || logoDragState.pointerId !== event.pointerId || !logoEditorImage || !logoConfig.crop) return;
  const point = canvasPointToImagePoint(event);
  const metrics = getLogoCanvasMetrics();
  if (!point || !metrics) return;
  const dx = (point.x - logoDragState.startX) / metrics.scale;
  const dy = (point.y - logoDragState.startY) / metrics.scale;
  logoConfig.crop = sanitizeLogoCrop({
    x: logoDragState.cropX + dx,
    y: logoDragState.cropY + dy,
    size: logoConfig.crop.size,
  }, logoEditorImage.naturalWidth, logoEditorImage.naturalHeight);
  renderLogoPreview();
  queueLogoRender();
}

function onLogoCanvasPointerUp(event) {
  if (!logoDragState || logoDragState.pointerId !== event.pointerId) return;
  logoDragState = null;
  if (logoEditorCanvas) {
    logoEditorCanvas.classList.remove('dragging');
    try {
      logoEditorCanvas.releasePointerCapture(event.pointerId);
    } catch (err) {
      console.debug('Pointer capture release skipped', err);
    }
  }
}

function centerLogoCrop() {
  if (!logoEditorImage || !logoConfig.crop) return;
  const width = logoEditorImage.naturalWidth;
  const height = logoEditorImage.naturalHeight;
  const size = logoConfig.crop.size;
  logoConfig.crop = sanitizeLogoCrop({
    x: (width - size) / 2,
    y: (height - size) / 2,
    size,
  }, width, height);
  renderLogoPreview();
  queueLogoRender();
}

function handleLogoCropSizeInput(event) {
  setLogoCropPercent(parseInt(event.target.value, 10) || 100);
  const label = document.getElementById('logo-crop-size-label');
  if (label) label.textContent = `${getLogoCropPercent()}%`;
  renderLogoPreview();
  queueLogoRender();
}

function triggerLogoFilePicker() {
  const input = document.getElementById('logo-file-input');
  if (input) input.click();
}

function loadLogoImage(src, crop) {
  if (!src) {
    logoConfig = { original_image: null, crop: null };
    logoEditorImage = null;
    logoEditorCanvas = null;
    logoEditorCtx = null;
    renderLogoButton();
    renderLogoEditor();
    return Promise.resolve();
  }
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      logoEditorImage = img;
      logoConfig = {
        original_image: src,
        crop: sanitizeLogoCrop(crop, img.naturalWidth, img.naturalHeight),
      };
      renderLogoEditor();
      resolve();
    };
    img.onerror = () => reject(new Error('Unable to load the selected image.'));
    img.src = src;
  });
}

function handleLogoFileInput(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = async () => {
    try {
      await loadLogoImage(reader.result, null);
    } catch (err) {
      alert(err.message || 'Unable to load that image.');
    }
  };
  reader.readAsDataURL(file);
}

function getCroppedLogoDataUrl(size = 128) {
  if (!logoEditorImage || !logoConfig.crop) return '';
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const crop = logoConfig.crop;
  ctx.drawImage(
    logoEditorImage,
    crop.x, crop.y, crop.size, crop.size,
    0, 0, size, size
  );
  return canvas.toDataURL('image/png');
}

async function fetchLogoConfig() {
  const response = await fetch('/api/app-logo');
  const data = await response.json();
  if (data.original_image) {
    await loadLogoImage(data.original_image, data.crop);
  } else {
    await loadLogoImage(null, null);
  }
  renderLogoButton();
}

async function openLogoModal() {
  try {
    await fetchLogoConfig();
  } catch (err) {
    console.error(err);
  }
  document.getElementById('logo-modal').classList.add('open');
  renderLogoEditor();
}

function closeLogoModal() {
  document.getElementById('logo-modal').classList.remove('open');
}

async function saveLogoConfig() {
  if (!logoConfig.original_image || !logoConfig.crop) return;
  const saveBtn = document.getElementById('logo-save-btn');
  saveBtn.disabled = true;
  const previousLabel = saveBtn.textContent;
  saveBtn.textContent = 'Saving…';
  try {
    await fetch('/api/app-logo', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(logoConfig),
    });
    renderLogoButton();
    closeLogoModal();
  } catch (err) {
    console.error(err);
    alert('Unable to save the app logo.');
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = previousLabel;
  }
}

function formatChartWindowLabel(sec) {
  if (sec < 3600) return (sec / 60) + ' min';
  const h = sec / 3600;
  if (h < 24) return h + (h === 1 ? ' hour' : ' hours');
  return (sec / 86400) + ' hours';
}

function navigate(section) {
  if (section !== 'services') stopSvcPoll();
  if (section !== 'debrid') stopDebridQueueMonitor();
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
  document.getElementById('section-' + section).classList.add('active');
  document.getElementById('tab-' + section).classList.add('active');
  currentSection = section;
  document.querySelector('.content').scrollTop = 0;
  if (section === 'overview') startHostStatsPoll();
  else stopHostStatsPoll();
  if (currentSection === 'overview') {
    loadOverview();
  } else if (currentSection === 'disks') {
    loadDrives();
  } else if (currentSection === 'services') {
    loadServices();
  } else if (currentSection === 'debrid') {
    loadDebridConfig();
  }
}

function refreshCurrent(useFresh = false) {
  if (currentSection === 'overview') loadOverview(!useFresh);
  else if (currentSection === 'disks') loadDrives(!useFresh);
  else if (currentSection === 'services') loadServices();
  else if (currentSection === 'debrid') loadDebridConfig();
}

function tempClass(t) {
  if (t==null) return '';
  if (t<40) return 'temp-cool';
  if (t<55) return 'temp-warm';
  return 'temp-hot';
}
function tempBarColor(t) {
  if (t==null) return '#5a6278';
  if (t<40) return '#00e5ff';
  if (t<55) return '#ffab00';
  return '#ff1744';
}
function tempBarWidth(t) {
  if (t==null) return '0%';
  return Math.min(100, Math.max(0, ((t-20)/60)*100)) + '%';
}
function formatGB(gb) {
  if (!gb) return '—';
  return gb >= 1000 ? (gb/1000).toFixed(1)+' TB' : gb+' GB';
}
function formatHours(h) {
  if (h==null) return '—';
  const d = Math.floor(h/24);
  return d > 0 ? `${d}d ${h%24}h` : `${h}h`;
}
function timeAgo(ts) {
  if (!ts) return 'Never';
  const diff = Math.floor((Date.now() - new Date(ts)) / 1000);
  if (diff < 60) return diff+'s ago';
  if (diff < 3600) return Math.floor(diff/60)+'m ago';
  if (diff < 86400) return Math.floor(diff/3600)+'h ago';
  return Math.floor(diff/86400)+'d ago';
}
function formatMs(ms) {
  if (ms == null) return '—';
  if (ms >= 60000) return (ms/1000).toFixed(0) + 's';
  return ms + 'ms';
}
function formatPercent(value) {
  if (!Number.isFinite(value)) return '—';
  return `${value.toFixed(1)}%`;
}
function formatBytes(bytes, decimals = 1) {
  if (!Number.isFinite(bytes)) return '—';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let index = 0;
  let normalized = bytes;
  while (normalized >= 1000 && index < units.length - 1) {
    normalized /= 1000;
    index += 1;
  }
  const useDecimals = index === 0 ? 0 : decimals;
  return `${normalized.toFixed(useDecimals)} ${units[index]}`;
}
function formatMemoryBytes(bytes, decimals = 1) {
  if (!Number.isFinite(bytes)) return '—';
  const units = ['B', 'KiB', 'MiB', 'GiB', 'TiB'];
  let index = 0;
  let normalized = bytes;
  while (normalized >= 1024 && index < units.length - 1) {
    normalized /= 1024;
    index += 1;
  }
  const useDecimals = index === 0 ? 0 : decimals;
  return `${normalized.toFixed(useDecimals)} ${units[index]}`;
}
function formatBytesPerSecond(bps) {
  if (!Number.isFinite(bps)) return '—';
  const units = ['B/s', 'KB/s', 'MB/s', 'GB/s'];
  let index = 0;
  let normalized = bps;
  while (normalized >= 1000 && index < units.length - 1) {
    normalized /= 1000;
    index += 1;
  }
  const labelValue = index === 0 ? normalized.toFixed(0) : normalized.toFixed(1);
  return `${labelValue} ${units[index]}`;
}
function formatTimeLabel(ts) {
  if (!ts) return null;
  return new Date(ts).toLocaleTimeString();
}
function setUpdated(timestamp) {
  const label = timestamp ? 'Updated ' + new Date(timestamp).toLocaleTimeString() : 'Never scanned';
  const textEl = document.getElementById('disks-updated-text');
  if (textEl) textEl.textContent = label;
}
function fetchHostStats() {
  return fetch('/api/system-stats')
    .then(r => r.json())
    .then(data => updateHostStats(data))
    .catch(err => {
      console.error('Failed to load host stats', err);
      updateHostStats(null);
    });
}

function startHostStatsPoll() {
  stopHostStatsPoll();
  fetchHostStats();
  hostStatsTimer = setInterval(fetchHostStats, 1000);
}

function stopHostStatsPoll() {
  if (hostStatsTimer) {
    clearInterval(hostStatsTimer);
    hostStatsTimer = null;
  }
}

function updateHostStats(stats) {
  const cpuEl = document.getElementById('host-stat-cpu-value');
  if (!cpuEl) return;
  stats = stats || {};
  const available = Boolean(stats.available);
  const statusLabel = available ? 'Live data' : (stats.error || 'Stats unavailable');

  const cpuValue = formatPercent(stats.cpu_percent);
  const ramValue = formatPercent(stats.memory_percent);
  const uploadValue = formatBytesPerSecond(stats.upload_bps);
  const downloadValue = formatBytesPerSecond(stats.download_bps);
  const derivedRamUsedBytes = Number.isFinite(stats.memory_percent) && Number.isFinite(stats.memory_total_bytes)
    ? Math.round((stats.memory_total_bytes * stats.memory_percent) / 100)
    : stats.memory_used_bytes;
  const usedMem = formatMemoryBytes(derivedRamUsedBytes);
  const totalMem = formatMemoryBytes(stats.memory_total_bytes);
  const ramSub = (usedMem === '—' && totalMem === '—') ? statusLabel : `Used ${usedMem} / ${totalMem}`;
  const uploadSub = Number.isFinite(stats.upload_bps) ? '' : statusLabel;
  const downloadSub = Number.isFinite(stats.download_bps) ? '' : statusLabel;

  const cpuValueEl = document.getElementById('host-stat-cpu-value');
  const ramValueEl = document.getElementById('host-stat-ram-value');
  const uploadValueEl = document.getElementById('host-stat-upload-value');
  const downloadValueEl = document.getElementById('host-stat-download-value');
  if (cpuValueEl) cpuValueEl.textContent = cpuValue;
  if (ramValueEl) ramValueEl.textContent = ramValue;
  if (uploadValueEl) uploadValueEl.textContent = uploadValue;
  if (downloadValueEl) downloadValueEl.textContent = downloadValue;
  const cpuSubEl = document.getElementById('host-stat-cpu-sub');
  const ramSubEl = document.getElementById('host-stat-ram-sub');
  if (cpuSubEl) cpuSubEl.textContent = available ? '' : statusLabel;
  if (ramSubEl) ramSubEl.textContent = ramSub;
  const uploadSubEl = document.getElementById('host-stat-upload-sub');
  const downloadSubEl = document.getElementById('host-stat-download-sub');
  if (uploadSubEl) uploadSubEl.textContent = uploadSub;
  if (downloadSubEl) downloadSubEl.textContent = downloadSub;
}
function setSpinning(on) {
  const btn = document.getElementById('disks-refresh-btn');
  if (!btn) return;
  btn.disabled = on;
  btn.setAttribute('aria-label', on ? 'Scanning drives' : 'Refresh drives');
  btn.title = on ? 'Scanning drives…' : 'Refresh drives';
  btn.classList.toggle('spinning', on);
}
function toggleServiceHistoryVisibility() {
  svcHistoryVisible = !svcHistoryVisible;
  applyServiceHistoryVisibility();
}
function applyServiceHistoryVisibility() {
  document.querySelectorAll('#services-container .chart-wrap').forEach(el => {
    el.classList.toggle('hidden', !svcHistoryVisible);
  });
  const icon = document.getElementById('services-history-icon');
  if (icon) icon.textContent = svcHistoryVisible ? 'expand_less' : 'expand_more';
  const btn = document.getElementById('services-history-btn');
  if (btn) {
    const label = svcHistoryVisible ? 'Hide service history' : 'Show service history';
    btn.title = label;
    btn.setAttribute('aria-label', label);
  }
}
function toggleDebridQueueVisibility() {
  debridQueueVisible = !debridQueueVisible;
  applyDebridQueueVisibility();
}
function applyDebridQueueVisibility() {
  const wrapper = document.getElementById('debrid-queue-wrapper');
  if (wrapper) wrapper.classList.toggle('hidden', !debridQueueVisible);
  const icon = document.getElementById('debrid-queue-toggle-icon');
  if (icon) icon.textContent = debridQueueVisible ? 'expand_less' : 'expand_more';
  const btn = document.getElementById('debrid-queue-toggle-btn');
  if (btn) {
    const label = debridQueueVisible ? 'Hide queue panel' : 'Show queue panel';
    btn.title = label;
    btn.setAttribute('aria-label', label);
  }
}
function normalizeServiceAddress(url) {
  const trimmed = String(url || '').trim();
  if (!trimmed) return '';
  if (/^[a-zA-Z][a-zA-Z\d+\-.]*:\/\//.test(trimmed)) return trimmed;
  return 'http://' + trimmed;
}
function openServiceAddress(url) {
  const target = normalizeServiceAddress(url);
  if (!target) return;
  window.open(target, '_blank', 'noopener');
}
function escapeHtml(str) {
  return String(str || '').replace(/[&<>"']/g, s => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[s]));
}
function svcVisualClass(status, responseMs) {
  return status || 'unknown';
}

let _liveTimerInterval = null;
function startLiveTimer() {
  if (_liveTimerInterval) return;
  _liveTimerInterval = setInterval(() => {
    document.querySelectorAll('[data-last-check-ts]').forEach(el => {
      el.textContent = timeAgo(el.dataset.lastCheckTs);
    });
  }, 10000);
}
startLiveTimer();

// ---- Overview ----

async function loadOverview(useCache = true) {
  setSpinning(true);
  try {
    const [dSum, sSum, drives, services] = await Promise.all([
      fetch(useCache ? '/api/drives/summary/cached' : '/api/drives/summary').then(r=>r.json()),
      fetch('/api/services/summary').then(r=>r.json()),
      fetch(useCache ? '/api/drives/cached' : '/api/drives').then(r=>r.json()),
      fetch('/api/services').then(r=>r.json()),
    ]);
    drivesCache = drives;
    servicesCache = services;

    await loadNicknames();
    renderOverviewDrives(drives);
    renderOverviewServices(services);
    setUpdated(dSum.last_scanned);
  } catch(e) { console.error(e); }
  setSpinning(false);
}

function renderOverviewDrives(drives) {
  const el = document.getElementById('ov-drives-list');
  if (!drives.length) { el.innerHTML = '<div style="color:var(--muted);font-size:13px">No drives found.</div>'; return; }
  el.innerHTML = drives.map(d => {
    const nick = nicknames[d.device] || d.model || 'Unknown';
    const temp = d.temperature != null ? `${d.temperature}°C` : '—';
    const tc = tempClass(d.temperature);
    return `<div class="overview-drive-row">
      <div>
        <div class="overview-drive-name">${nick}</div>
        <div class="overview-drive-meta">${d.device} · ${formatGB(d.capacity_gb)}</div>
      </div>
      <div style="display:flex;align-items:center;gap:10px">
        <span class="${tc}" style="font-weight:600;font-size:13px">${temp}</span>
        <span class="health-badge ${d.health}">${d.health}</span>
      </div>
    </div>`;
  }).join('');
}

function renderOverviewServices(services) {
  const el = document.getElementById('ov-services-list');
  if (!services.length) {
    el.innerHTML = '<div style="color:var(--muted);font-size:13px">No services added. <button class="panel-link" onclick="navigate(\'services\')">Add one →</button></div>';
    return;
  }
  el.innerHTML = services.map(s => {
    const st = s.latest ? s.latest.status : 'unknown';
    const vc = svcVisualClass(st, s.latest?.response_ms);
    const ts = s.latest?.timestamp || '';
    const statusLabel = st === 'unknown' ? '—' : st.toUpperCase();
    const badgeLabel = `<span class="badge-icon material-icons icon-inline">public</span>${statusLabel}`;
    const hasExternal = !!s.url;
    const hasLocal = !!s.local_url;
    const lst = hasLocal ? (s.latest_local ? s.latest_local.status : 'unknown') : null;
    const localStatusLabel = lst === 'unknown' ? '—' : lst.toUpperCase();
    const badges = [];
    if (hasExternal) badges.push(`<span class="svc-badge ext-badge ${vc}" title="External">${badgeLabel}</span>`);
    if (hasLocal) badges.push(`<span class="svc-badge local-badge ${lst}" title="Local"><span class="badge-icon material-icons icon-inline">home</span>${localStatusLabel}</span>`);
    return `<div class="overview-service-row">
      <div class="status-dot ${vc}"></div>
      <div style="flex:1">
        <div style="font-weight:500;font-size:13px">${s.name}</div>
        <div style="font-size:11px;color:var(--muted)" data-last-check-ts="${ts}">${timeAgo(ts)}</div>
      </div>
      <div style="display:flex;align-items:center;gap:6px">
        ${badges.join('')}
      </div>
    </div>`;
  }).join('');
}

async function loadNicknames() {
  const resp = await fetch('/api/nicknames');
  nicknames = await resp.json();
}

// ---- Drives ----

async function loadDrives(useCache = true) {
  setSpinning(true);
  try {
    await loadNicknames();
    const [dSum, drives] = await Promise.all([
      fetch(useCache ? '/api/drives/summary/cached' : '/api/drives/summary').then(r=>r.json()),
      fetch(useCache ? '/api/drives/cached' : '/api/drives').then(r=>r.json()),
    ]);
    drivesCache = drives;
    document.getElementById('s-total').textContent = drives.length;
    document.getElementById('s-healthy').textContent = drives.filter(d=>d.health==='PASS').length;
    document.getElementById('s-failing').textContent = drives.filter(d=>d.health==='FAIL').length;
    const temps = drives.filter(d=>d.temperature!=null).map(d=>d.temperature);
    document.getElementById('s-temp').textContent = temps.length ? Math.round(temps.reduce((a,b)=>a+b,0)/temps.length)+'°C' : '—';
    const container = document.getElementById('drives-container');
    if (!drives.length) {
      container.innerHTML = `<div class="empty-state"><div class="empty-icon"><span class="material-icons">storage</span></div><p>No drives detected. Make sure smartmontools is installed and running as Administrator.</p></div>`;
    } else {
      drivesCache = drives;
      renderDrivesGrid(drives);
    }
    setUpdated(dSum.last_scanned);
  } catch(e) {
    document.getElementById('drives-container').innerHTML = `<div class="empty-state"><p style="color:var(--fail)">Failed to scan drives: ${e.message}</p></div>`;
  }
  setSpinning(false);
}

function renderDrive(drive, idx) {
  const id = `drive-${idx}`;
  const tempNum = drive.temperature!=null ? drive.temperature+'°C' : 'N/A';
  const tc = tempClass(drive.temperature);
  const icon = drive.type==='NVMe'?'flash_on':drive.type==='SSD'?'sd_storage':'storage';
  const failedAttrs = (drive.attributes||[]).filter(a=>a.failed);
  const savedNick = nicknames[drive.device];
  const displayName = savedNick || drive.model || 'Unknown Drive';

  let attrsHTML = drive.attributes && drive.attributes.length > 0
    ? `<table class="attrs-table"><thead><tr><th>Attribute</th><th>Value</th><th>Worst</th><th>Thresh</th><th>Raw</th></tr></thead><tbody>
        ${drive.attributes.map(a=>`<tr class="${a.failed?'attr-failed':''}"><td>${a.name}</td><td>${a.value??'—'}</td><td>${a.worst??'—'}</td><td>${a.thresh??'—'}</td><td class="attr-raw">${a.raw??'—'}</td></tr>`).join('')}
       </tbody></table>`
    : '<div style="color:var(--muted);font-size:12px;padding:8px 0">No SMART attributes available</div>';

  return `<div class="drive-card ${drive.health==='FAIL'?'fail-card':''}" style="animation-delay:${idx*0.06}s" data-device="${drive.device}">
    <div class="drive-header">
      <div class="drive-title">
        <span class="drive-icon material-icons">${icon}</span>
        <div>
          <div style="display:flex;align-items:center;gap:6px">
            <span class="drive-nickname" id="${id}-display-name">${displayName}</span>
            <button class="rename-btn" onclick="toggleRename('${id}')" title="Rename"><span class="material-icons">edit</span></button>
          </div>
          <span style="display:none" id="${id}-model-name">${drive.model||'Unknown Drive'}</span>
          <div class="rename-input-row" id="${id}-rename-row">
            <input class="rename-input" id="${id}-rename-input" type="text" placeholder="Custom name…" value="${savedNick||''}"
              onkeydown="if(event.key==='Enter')saveNickname('${id}','${drive.device}');if(event.key==='Escape')cancelRename('${id}')"/>
            <button class="rename-save" onclick="saveNickname('${id}','${drive.device}')">Save</button>
            <button class="rename-cancel" onclick="cancelRename('${id}')">✕</button>
          </div>
        </div>
      </div>
      <span class="health-badge ${drive.health}">${drive.health}</span>
    </div>
    <div class="drive-body">
      <div class="drive-meta">
        <div><div class="meta-label">Type</div><div class="meta-value">${drive.type||'—'}</div></div>
        <div><div class="meta-label">Capacity</div><div class="meta-value">${formatGB(drive.capacity_gb)}</div></div>
        <div><div class="meta-label">Serial</div><div class="meta-value" style="font-family:var(--mono);font-size:11px;letter-spacing:0.06em">${drive.serial||'—'}</div></div>
        <div><div class="meta-label">Power On</div><div class="meta-value">${formatHours(drive.power_on_hours)}</div></div>
      </div>
      ${drive.temperature!=null?`
      <div class="temp-row">
        <div class="temp-number ${tc}">${tempNum}</div>
        <div class="temp-bar-wrap">
          <div class="temp-bar-label">TEMPERATURE · 20°C ————— 80°C</div>
          <div class="temp-bar-track"><div class="temp-bar-fill" style="width:${tempBarWidth(drive.temperature)};background:${tempBarColor(drive.temperature)}"></div></div>
        </div>
      </div>`:''}
      ${failedAttrs.length>0?`<div style="background:rgba(255,23,68,0.08);border:1px solid rgba(255,23,68,0.25);border-radius:6px;padding:10px 12px;margin-bottom:10px;font-size:12px;color:var(--fail)">⚠ ${failedAttrs.length} failing attribute${failedAttrs.length>1?'s':''}: ${failedAttrs.map(a=>a.name).join(', ')}</div>`:''}
      <button class="expand-btn" onclick="toggleAttrs('${id}')">▼ SMART Attributes</button>
      <div class="attrs-section" id="${id}-attrs">${attrsHTML}</div>
      <button class="expand-btn" onclick="toggleHistory('${id}','${drive.device}')" style="margin-top:4px">▼ Temperature History</button>
      <div class="history-section" id="${id}-history">
        <div class="chart-wrap"><div class="chart-title">Temperature over time (°C)</div><canvas id="${id}-chart" height="80"></canvas></div>
      </div>
  </div>
</div>`;
}

function renderDrivesGrid(drives) {
  const container = document.getElementById('drives-container');
  if (!container) return;
  container.innerHTML = `<div class="drives-grid">${drives.map(renderDrive).join('')}</div>`;
}

let reorderState = { type: null, items: [] };

async function saveServiceOrder(orderIds) {
  const order = orderIds || Array.from(document.querySelectorAll('#services-container .services-grid .service-card')).map(item => Number(item.dataset.id));
  await fetch('/api/services/order', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({order})
  });
}

function openReorderModal(type) {
  reorderState.type = type;
  const items = (type === 'drives' ? drivesCache : servicesCache) || [];
  reorderState.items = items.slice();
  const titleEl = document.getElementById('reorder-modal-title');
  const subtitleEl = document.getElementById('reorder-modal-subtitle');
  if (titleEl) titleEl.textContent = type === 'drives' ? 'Reorder Drives' : 'Reorder Services';
  if (subtitleEl) {
    subtitleEl.textContent = type === 'drives'
      ? 'Drives order is saved persistently and applies after every scan.'
      : 'Service order is saved to the server and affects the Services page.';
  }
  renderReorderList();
  document.getElementById('reorder-modal')?.classList.add('open');
}

function renderReorderList() {
  const list = document.getElementById('reorder-list');
  if (!list) return;
  const items = reorderState.items || [];
  if (!items.length) {
    list.innerHTML = `<li class="reorder-item"><span class="reorder-label">Nothing to reorder yet.</span></li>`;
    return;
  }
  const type = reorderState.type;
  list.innerHTML = items.map((item, idx) => {
    const label = type === 'drives'
      ? `${escapeHtml(nicknames[item.device] || item.model || 'Unknown Drive')} · ${escapeHtml(item.device)}`
      : escapeHtml(item.name || 'Unnamed service');
    const meta = type === 'drives'
      ? escapeHtml(item.device)
      : escapeHtml(item.url || item.local_url || 'Local monitor');
    return `<li class="reorder-item">
      <div>
        <div class="reorder-label">${label}</div>
        <div class="reorder-meta">${meta}</div>
      </div>
      <div class="reorder-controls">
        <button type="button" onclick="moveReorderItem(${idx}, -1)" ${idx === 0 ? 'disabled' : ''}><span class="material-icons">arrow_upward</span></button>
        <button type="button" onclick="moveReorderItem(${idx}, 1)" ${idx === items.length - 1 ? 'disabled' : ''}><span class="material-icons">arrow_downward</span></button>
      </div>
    </li>`;
  }).join('');
}

function moveReorderItem(index, delta) {
  const items = reorderState.items;
  if (!items || !items.length) return;
  const target = index + delta;
  if (target < 0 || target >= items.length) return;
  [items[index], items[target]] = [items[target], items[index]];
  renderReorderList();
}

function closeReorderModal() {
  reorderState.type = null;
  reorderState.items = [];
  document.getElementById('reorder-modal')?.classList.remove('open');
}

async function saveReorderChanges() {
  if (!reorderState.type) return closeReorderModal();
  if (reorderState.type === 'drives') {
    drivesCache = reorderState.items.slice();
    renderDrivesGrid(drivesCache);
    const order = drivesCache.map(item => item.device);
    try {
      const resp = await fetch('/api/drives/order', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({order})
      });
      if (!resp.ok) {
        const payload = await resp.json().catch(() => null);
        throw new Error(payload?.error || resp.statusText || 'Unknown error');
      }
    } catch (err) {
      console.error('Failed to save drive order', err);
      alert('Unable to save drive order. Please try again.');
    }
  } else {
    const order = reorderState.items.map(item => item.id);
    if (order.length) await saveServiceOrder(order);
    await loadServices(true);
  }
  closeReorderModal();
}

function toggleAttrs(id) {
  const el = document.getElementById(id+'-attrs');
  el.classList.toggle('open');
  el.previousElementSibling.textContent = el.classList.contains('open') ? '▲ SMART Attributes' : '▼ SMART Attributes';
}
async function toggleHistory(id, device) {
  const el = document.getElementById(id+'-history');
  el.classList.toggle('open');
  el.previousElementSibling.textContent = el.classList.contains('open') ? '▲ Temperature History' : '▼ Temperature History';
  if (el.classList.contains('open') && !charts[id]) await loadDriveHistory(id, device);
}
async function loadDriveHistory(id, device) {
  const data = await fetch(`/api/history/${device.replace(/^\//,'')}`).then(r=>r.json());
  const canvas = document.getElementById(id+'-chart');
  if (!canvas || !data.length) return;
  charts[id] = new Chart(canvas, {
    type: 'line',
    data: { labels: data.map(d=>new Date(d.timestamp).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})),
      datasets: [{ data: data.map(d=>d.temperature), borderColor:'#00e5ff', backgroundColor:'rgba(0,229,255,0.06)', borderWidth:2, pointRadius:3, pointBackgroundColor:'#00e5ff', fill:true, tension:0.4 }] },
    options: { responsive:true, plugins:{legend:{display:false}}, scales:{ x:{ticks:{color:'#5a6278',font:{family:'DM Mono',size:9}},grid:{color:'#1f2530'}}, y:{ticks:{color:'#5a6278',font:{family:'DM Mono',size:9}},grid:{color:'#1f2530'}} } }
  });
}

function toggleRename(id) {
  const row = document.getElementById(id+'-rename-row');
  row.classList.toggle('open');
  if (row.classList.contains('open')) document.getElementById(id+'-rename-input').focus();
}
async function saveNickname(id, device) {
  const nickname = document.getElementById(id+'-rename-input').value.trim();
  await fetch('/api/nickname', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({device,nickname}) });
  nicknames[device] = nickname;
  const nameEl = document.getElementById(id+'-display-name');
  if (nameEl) nameEl.textContent = nickname || document.getElementById(id+'-model-name').textContent;
  document.getElementById(id+'-rename-row').classList.remove('open');
}
function cancelRename(id) { document.getElementById(id+'-rename-row').classList.remove('open'); }

// ---- Services ----

let _svcPollTimer = null;
function startSvcPoll() { stopSvcPoll(); _svcPollTimer = setInterval(softRefreshServices, 15000); }
function stopSvcPoll() { if (_svcPollTimer) { clearInterval(_svcPollTimer); _svcPollTimer = null; } }

async function softRefreshServices() {
  try {
    const services = await fetch('/api/services').then(r=>r.json());
    servicesCache = services;
    updateServiceSummary(services);
    for (const svc of services) {
      const card = document.getElementById(`svc-card-${svc.id}`);
      if (!card) continue;
      updateServiceCard(card, svc);
    }
  } catch(e) { console.error(e); }
}

function updateServiceSummary(services) {
  const totalUp = services.filter(s => s.latest?.status === 'up').length;
  const totalDown = services.filter(s => s.latest?.status === 'down').length;
  document.getElementById('ss-up').textContent = totalUp;
  document.getElementById('ss-down').textContent = totalDown;
}

function buildHistoryDots(recentHistory) {
  const dots = Array(30).fill('unknown');
  if (recentHistory && recentHistory.length) {
    const slots = recentHistory.slice(-30);
    slots.forEach((d, i) => { dots[30 - slots.length + i] = svcVisualClass(d.status, d.response_ms); });
  }
  return dots;
}

function trimChartToWindow(chart, windowMs) {
  if (!chart.data.labels.length) return;
  const firstTs = new Date(chart.data.labels[0]).getTime();
  const cutoff = Date.now() - windowMs;
  if (firstTs >= cutoff) return;
  while (chart.data.labels.length > 1 && new Date(chart.data.labels[0]).getTime() < cutoff) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update('none');
}

function updateServiceCard(card, svc) {
  const st = svc.latest ? svc.latest.status : 'unknown';
  const vc = svcVisualClass(st, svc.latest?.response_ms);
  const ms = svc.latest?.response_ms != null ? formatMs(svc.latest.response_ms) : '—';
  const uptime = svc.uptime != null ? svc.uptime + '%' : '—';
  const ts = svc.latest?.timestamp || '';
  const windowSec = svc.chart_window_sec || 2700;
  const hasLocal = !!svc.local_url;
  const lst = hasLocal ? (svc.latest_local ? svc.latest_local.status : 'unknown') : null;

  card.className = `service-card${vc === 'down' ? ' svc-down' : ''}`;

  const dot = card.querySelector('.status-dot');
  if (dot) dot.className = `status-dot ${vc}`;

  const extBadge = card.querySelector('.svc-badge.ext-badge');
  if (extBadge) {
    extBadge.className = `svc-badge ext-badge ${vc}`;
    const statusLabel = st === 'unknown' ? '—' : st.toUpperCase();
    extBadge.innerHTML = `<span class="badge-icon material-icons icon-inline">public</span>${statusLabel}`;
  }

  const localBadge = card.querySelector('.svc-badge.local-badge');
  if (localBadge && hasLocal) {
    localBadge.className = `svc-badge local-badge ${lst}`;
    const localLabel = lst === 'unknown' ? '—' : lst.toUpperCase();
    localBadge.innerHTML = `<span class="badge-icon material-icons icon-inline">home</span>${localLabel}`;
  }

  card.querySelectorAll('.svc-meta-item').forEach(item => {
    const label = item.querySelector('.meta-label')?.textContent?.trim();
    const val = item.querySelector('.meta-value');
    if (!val) return;
    if (label === 'Response') {
      val.textContent = ms;
      val.className = 'meta-value';
    }
    if (label === 'Uptime') val.textContent = uptime;
    if (label === 'Last Check') {
      val.setAttribute('data-last-check-ts', ts);
      val.textContent = timeAgo(ts);
    }
  });

  const bar = document.getElementById(`svc-bar-ext-${svc.id}`);
  if (bar) {
    const dots = buildHistoryDots(svc.recent_history);
    bar.innerHTML = dots.map(s => `<div class="hb-dot ${s}" title="${s}"></div>`).join('');
  }

  const localBar = document.getElementById(`svc-bar-local-${svc.id}`);
  if (localBar && hasLocal) {
    const dots = buildHistoryDots(svc.recent_history_local);
    localBar.innerHTML = dots.map(s => `<div class="hb-dot ${s}" title="${s}"></div>`).join('');
  }

  const extChart = charts[`svc-ext-${svc.id}`];
  if (extChart && svc.latest?.response_ms != null && svc.latest?.timestamp) {
    const label = new Date(svc.latest.timestamp).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
    const lastLabel = extChart.data.labels[extChart.data.labels.length - 1];
    if (label !== lastLabel) {
      extChart.data.labels.push(label);
      extChart.data.datasets[0].data.push(svc.latest.response_ms);
      trimChartToWindow(extChart, windowSec * 1000);
    }
  }

  const localChart = charts[`svc-local-${svc.id}`];
  if (localChart && svc.latest_local?.response_ms != null && svc.latest_local?.timestamp) {
    const label = new Date(svc.latest_local.timestamp).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
    const lastLabel = localChart.data.labels[localChart.data.labels.length - 1];
    if (label !== lastLabel) {
      localChart.data.labels.push(label);
      localChart.data.datasets[0].data.push(svc.latest_local.response_ms);
      trimChartToWindow(localChart, windowSec * 1000);
    }
  }
}

async function loadServices(silent) {
  try {
    const services = await fetch('/api/services').then(r=>r.json());
    servicesCache = services;
    updateServiceSummary(services);
    const container = document.getElementById('services-container');
    if (!services.length) {
      container.innerHTML = `<div class="empty-state"><div class="empty-icon"><span class="material-icons">public</span></div><p>No services yet. Click <strong>+ Add Service</strong> to start monitoring.</p></div>`;
    } else {
      container.innerHTML = `<div class="services-grid">${services.map(renderService).join('')}</div>`;
      await Promise.all(services.map(s => loadSvcHistoryCharts(s.id)));
    }
    applyServiceHistoryVisibility();
    startSvcPoll();
  } catch(e) { console.error(e); }
}

function renderService(svc, idx) {
  const st = svc.latest ? svc.latest.status : 'unknown';
  const vc = svcVisualClass(st, svc.latest?.response_ms);
  const ms = svc.latest?.response_ms != null ? formatMs(svc.latest.response_ms) : '—';
  const uptime = svc.uptime != null ? svc.uptime+'%' : '—';
  const ts = svc.latest?.timestamp || '';
  const hasExternal = !!svc.url;
  const extDots = hasExternal ? buildHistoryDots(svc.recent_history) : [];
  const statusLabel = st === 'unknown' ? '—' : st.toUpperCase();
  const badgeLabel = `<span class="badge-icon material-icons icon-inline">public</span>${statusLabel}`;
  const windowLabel = formatChartWindowLabel(svc.chart_window_sec || 2700);

  const hasLocal = !!svc.local_url;
  const lst = hasLocal ? (svc.latest_local ? svc.latest_local.status : 'unknown') : null;
  const localDots = hasLocal ? buildHistoryDots(svc.recent_history_local) : [];
  const localMs = hasLocal && svc.latest_local?.response_ms != null ? formatMs(svc.latest_local.response_ms) : null;

  const localLabel = lst === 'unknown' ? '—' : lst.toUpperCase();
  const localBadgeHtml = hasLocal
    ? `<span class="svc-badge local-badge ${lst}"><span class="badge-icon material-icons icon-inline">home</span>${localLabel}</span>`
    : '';
  const extBadgeHtml = hasExternal
    ? `<span class="svc-badge ext-badge ${vc}">${badgeLabel}</span>`
    : '';

  const localBarHtml = hasLocal ? `
    <div class="bar-row">
      <div class="bar-row-label">
        <div class="bar-row-label-left">
          <span class="bar-tag loc">Local</span>
          <span class="svc-link" onclick="openServiceAddress('${escapeHtml(svc.local_url)}')">${escapeHtml(svc.local_url)}</span>
        </div>
        <span>${localMs || '—'}</span>
      </div>
      <div class="history-bar local" id="svc-bar-local-${svc.id}">
        ${localDots.map(s=>`<div class="hb-dot ${s}" title="${s}"></div>`).join('')}
      </div>
    </div>` : '';

  const localChartHtml = hasLocal ? `
    <div class="chart-wrap">
      <div class="chart-title"><span class="material-icons icon-inline">home</span>Local — ${windowLabel} (ms)</div>
      <canvas id="svc-local-chart-${svc.id}" height="60"></canvas>
    </div>` : '';

  const extSectionHtml = hasExternal ? `
        <div class="bar-row">
          <div class="bar-row-label">
            <div class="bar-row-label-left">
              <span class="bar-tag ext">External</span>
              <span class="svc-link" onclick="openServiceAddress('${escapeHtml(svc.url)}')">${escapeHtml(svc.url)}</span>
            </div>
            <span>${ms}</span>
          </div>
          <div class="history-bar" id="svc-bar-ext-${svc.id}">
            ${extDots.map(s=>`<div class="hb-dot ${s}" title="${s}"></div>`).join('')}
          </div>
        </div>` : '';

  const extChartHtml = hasExternal ? `
        <div class="chart-wrap">
          <div class="chart-title"><span class="material-icons icon-inline">public</span>External — ${windowLabel} (ms)</div>
          <canvas id="svc-ext-chart-${svc.id}" height="60"></canvas>
        </div>` : '';

  const extGroupHtml = hasExternal ? `
      <div class="svc-data-group external">
        ${extSectionHtml}
        ${extChartHtml}
      </div>` : '';

  const localGroupHtml = hasLocal ? `
      <div class="svc-data-group local">
        ${localBarHtml}
        ${localChartHtml}
      </div>` : '';

  return `<div class="service-card ${vc==='down'?'svc-down':''}" style="animation-delay:${idx*0.05}s" id="svc-card-${svc.id}" data-id="${svc.id}">
    <div class="service-header">
      <div class="service-title-row">
        <div class="status-dot ${vc}"></div>
        <div>
          <div class="service-name service-title-clickable" onclick="openEditModal(${svc.id})" style="cursor:pointer">${svc.name}</div>
        </div>
      </div>
      <div class="svc-badges">
        ${extBadgeHtml}
        ${localBadgeHtml}
      </div>
    </div>
    <div class="service-body">
      <div class="service-meta-row">
        <div class="svc-meta-item"><div class="meta-label">Response</div><div class="meta-value">${ms}</div></div>
        <div class="svc-meta-item"><div class="meta-label">Uptime</div><div class="meta-value">${uptime}</div></div>
        <div class="svc-meta-item"><div class="meta-label">Last Check</div><div class="meta-value" style="font-size:12px" data-last-check-ts="${ts}">${timeAgo(ts)}</div></div>
        <div class="svc-meta-item"><div class="meta-label">Interval</div><div class="meta-value">${svc.interval}s</div></div>
      </div>

      <div class="service-data-groups" id="svc-charts-${svc.id}">
        ${extGroupHtml}
        ${localGroupHtml}
      </div>
    </div>
  </div>`;
}

async function loadSvcHistoryCharts(svcId) {
  const el = document.getElementById(`svc-charts-${svcId}`);
  if (!el) return;

  const svc = servicesCache.find(s => s.id === svcId);
  const windowSec = svc ? (svc.chart_window_sec || 2700) : 2700;
  const windowMs = windowSec * 1000;
  const cutoff = Date.now() - windowMs;

  ['svc-ext', 'svc-local'].forEach(prefix => {
    const key = `${prefix}-${svcId}`;
    if (charts[key]) { charts[key].destroy(); delete charts[key]; }
  });

  const [extData, localData] = await Promise.all([
    fetch(`/api/services/${svcId}/history?target=external`).then(r=>r.json()),
    svc?.local_url ? fetch(`/api/services/${svcId}/history?target=local`).then(r=>r.json()) : Promise.resolve([]),
  ]);

  const extBar = document.getElementById(`svc-bar-ext-${svcId}`);
  if (extBar && extData.length) {
    const slots = extData.slice(-30);
    const dots = Array(30).fill('unknown');
    slots.forEach((d,i) => { dots[30-slots.length+i] = svcVisualClass(d.status, d.response_ms); });
    extBar.innerHTML = dots.map(s=>`<div class="hb-dot ${s}"></div>`).join('');
  }
  if (svc?.local_url) {
    const localBar = document.getElementById(`svc-bar-local-${svcId}`);
    if (localBar && localData.length) {
      const slots = localData.slice(-30);
      const dots = Array(30).fill('unknown');
      slots.forEach((d,i) => { dots[30-slots.length+i] = svcVisualClass(d.status, d.response_ms); });
      localBar.innerHTML = dots.map(s=>`<div class="hb-dot ${s}"></div>`).join('');
    }
  }

  function buildChart(canvasId, data, color) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const filtered = data.filter(d => d.response_ms != null && new Date(d.timestamp).getTime() >= cutoff);
    const pointColors = filtered.map(() => color);
    return new Chart(canvas, {
      type: 'line',
      data: {
        labels: filtered.map(d => new Date(d.timestamp).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})),
        datasets: [{
          data: filtered.map(d => d.response_ms),
          borderColor: color, backgroundColor: color + '0d',
          borderWidth: 2, pointRadius: 3,
          pointBackgroundColor: pointColors, pointBorderColor: pointColors,
          fill: true, tension: 0.4,
          segment: { borderColor: color }
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: '#5a6278', font: { family: 'DM Mono', size: 9 } }, grid: { color: '#1f2530' } },
          y: { ticks: { color: '#5a6278', font: { family: 'DM Mono', size: 9 } }, grid: { color: '#1f2530' } }
        }
      }
    });
  }

  const extChart = buildChart(`svc-ext-chart-${svcId}`, extData, '#00e5ff');
  if (extChart) charts[`svc-ext-${svcId}`] = extChart;

  if (svc?.local_url) {
    const localChart = buildChart(`svc-local-chart-${svcId}`, localData, '#a78bfa');
    if (localChart) charts[`svc-local-${svcId}`] = localChart;
  }
}

async function deleteServiceFromModal() {
  if (!confirm('Are you sure you want to remove this service monitor?')) return;
  await fetch(`/api/services/${_editingServiceId}`, {method:'DELETE'});
  closeAddModal();
  stopSvcPoll();
  await loadServices();
}

async function deleteService(svcId) {
  if (!confirm('Remove this service monitor?')) return;
  await fetch(`/api/services/${svcId}`, {method:'DELETE'});
  stopSvcPoll();
  await loadServices();
}

let _editingServiceId = null;

function openAddModal() {
  _editingServiceId = null;
  document.getElementById('modal-title').textContent = 'Add Service Monitor';
  document.getElementById('modal-submit-btn').textContent = 'Add Service';
  document.getElementById('modal-delete-btn').style.display = 'none';
  document.getElementById('svc-name').value = '';
  document.getElementById('svc-url').value = '';
  document.getElementById('svc-type').value = 'http';
  document.getElementById('svc-interval').value = '60';
  document.getElementById('svc-chart-window').value = '2700';
  document.getElementById('svc-local-url').value = '';
  document.getElementById('svc-local-type').value = 'tcp';
  document.getElementById('add-modal').classList.add('open');
}

function openEditModal(svcId) {
  const svc = servicesCache.find(s => s.id === svcId);
  if (!svc) return;
  _editingServiceId = svcId;
  document.getElementById('modal-title').textContent = 'Edit Service';
  document.getElementById('modal-submit-btn').textContent = 'Save Changes';
  document.getElementById('modal-delete-btn').style.display = 'block';
  document.getElementById('svc-name').value = svc.name;
  document.getElementById('svc-url').value = svc.url;
  document.getElementById('svc-type').value = svc.check_type;
  document.getElementById('svc-interval').value = svc.interval;
  document.getElementById('svc-chart-window').value = String(svc.chart_window_sec || 2700);
  document.getElementById('svc-local-url').value = svc.local_url || '';
  document.getElementById('svc-local-type').value = svc.local_check_type || 'tcp';
  document.getElementById('add-modal').classList.add('open');
}

function closeAddModal() {
  document.getElementById('add-modal').classList.remove('open');
  _editingServiceId = null;
}
document.getElementById('add-modal').addEventListener('click', e => { if(e.target===e.currentTarget) closeAddModal(); });
document.getElementById('reorder-modal').addEventListener('click', e => { if(e.target===e.currentTarget) closeReorderModal(); });
document.getElementById('logo-modal').addEventListener('click', e => { if(e.target===e.currentTarget) closeLogoModal(); });
document.getElementById('debrid-modal').addEventListener('click', e => { if(e.target===e.currentTarget) closeDebridModal(); });

async function submitAddService() {
  const name = document.getElementById('svc-name').value.trim();
  const url = document.getElementById('svc-url').value.trim();
  const type = document.getElementById('svc-type').value;
  const interval = parseInt(document.getElementById('svc-interval').value) || 60;
  const chartWindowSec = parseInt(document.getElementById('svc-chart-window').value) || 2700;
  const localUrl = document.getElementById('svc-local-url').value.trim();
  const localType = document.getElementById('svc-local-type').value;
  if (!name || !localUrl) { alert('Name and Local IP/Host are required.'); return; }

  const submitBtn = document.getElementById('modal-submit-btn');
  const cancelBtn = submitBtn.previousElementSibling;
  submitBtn.disabled = true;
  cancelBtn.disabled = true;
  submitBtn.textContent = _editingServiceId ? 'Saving…' : 'Checking…';

  const payload = { name, url: url || "", check_type: type, interval, chart_window_sec: chartWindowSec,
                    local_url: localUrl, local_check_type: localType };

  try {
    if (_editingServiceId) {
      await fetch(`/api/services/${_editingServiceId}`, {
        method: 'PATCH', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      await fetch(`/api/services/${_editingServiceId}/check`, {method: 'POST'});
    } else {
      const res = await fetch('/api/services', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const {id} = await res.json();
      await fetch(`/api/services/${id}/check`, {method: 'POST'});
    }
  } finally {
    submitBtn.disabled = false;
    cancelBtn.disabled = false;
    submitBtn.textContent = _editingServiceId ? 'Save Changes' : 'Add Service';
  }

  closeAddModal();
  stopSvcPoll();
  await loadServices();
}

function renderDebridInfo() {
  const statusEl = document.getElementById('debrid-status');
  if (statusEl) statusEl.textContent = debridConfig.ip ? 'Configured' : 'Not configured';
}

function setDebridMagnetStatus(message, tone) {
  const statusEl = document.getElementById('debrid-magnet-status');
  if (!statusEl) return;
  statusEl.textContent = message || '';
  statusEl.classList.toggle('success', tone === 'success');
  statusEl.classList.toggle('error', tone === 'error');
  if (magnetStatusTimer) {
    clearTimeout(magnetStatusTimer);
    magnetStatusTimer = null;
  }
  if (message) {
    magnetStatusTimer = setTimeout(() => {
      statusEl.textContent = '';
      statusEl.classList.remove('success', 'error');
      magnetStatusTimer = null;
    }, 5000);
  }
}

async function submitMagnetLink(magnetLink, inputElement) {
  const candidate = (magnetLink || '').trim();
  if (!candidate) {
    setDebridMagnetStatus('Paste a magnet link to queue it.', 'error');
    return;
  }
  if (!candidate.toLowerCase().startsWith('magnet:?')) {
    setDebridMagnetStatus('Only magnet links are supported.', 'error');
    return;
  }
  if (!debridConfig.ip || !debridConfig.username) {
    setDebridMagnetStatus('Configure the Debrid client before queuing.', 'error');
    return;
  }
  if (magnetSubmissionInProgress) {
    setDebridMagnetStatus('Already sending a magnet link. Please wait.', 'error');
    return;
  }

  magnetSubmissionInProgress = true;
  if (inputElement) inputElement.disabled = true;
  setDebridMagnetStatus('Sending magnet link…');
  try {
    const resp = await fetch('/api/debrid-ingest-magnet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ magnetLink: candidate }),
    });
    const payload = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      const message = payload.error || payload.detail || 'Proxy error';
      throw new Error(message);
    }
    setDebridMagnetStatus('Magnet queued for ingestion!', 'success');
    if (inputElement) inputElement.value = '';
  } catch (err) {
    console.error('Failed to submit magnet link', err);
    setDebridMagnetStatus(err.message || 'Unable to queue magnet link', 'error');
  } finally {
    magnetSubmissionInProgress = false;
    if (inputElement) inputElement.disabled = false;
  }
}

function handleMagnetPaste(event) {
  const input = event.target;
  setTimeout(() => {
    const value = (input?.value || '').trim();
    if (value) {
      submitMagnetLink(value, input);
    }
  }, 0);
}

function setupDebridMagnetInput() {
  const input = document.getElementById('debrid-magnet-input');
  if (!input) return;
  input.addEventListener('paste', handleMagnetPaste);
  input.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
      event.preventDefault();
      submitMagnetLink((input.value || '').trim(), input);
    }
  });
}

async function loadDebridConfig() {
  try {
    const resp = await fetch('/api/debrid-config');
    if (!resp.ok) throw new Error('Failed to load Debrid settings');
    debridConfig = await resp.json() || { ip: '', username: '', password: '', updated_at: null };
    renderDebridInfo();
    if (currentSection === 'debrid') startDebridQueueMonitor();
  } catch (err) {
    console.error('Failed to load debrid config', err);
  }
}

function openDebridModal() {
  document.getElementById('debrid-ip-input').value = debridConfig.ip || '';
  document.getElementById('debrid-username-input').value = debridConfig.username || '';
  document.getElementById('debrid-password-input').value = debridConfig.password || '';
  document.getElementById('debrid-modal').classList.add('open');
}

function closeDebridModal() {
  document.getElementById('debrid-modal').classList.remove('open');
}

async function submitDebridConfig() {
  const btn = document.getElementById('debrid-save-btn');
  const payload = {
    ip: document.getElementById('debrid-ip-input').value.trim(),
    username: document.getElementById('debrid-username-input').value.trim(),
    password: document.getElementById('debrid-password-input').value,
  };
  btn.disabled = true;
  try {
    const resp = await fetch('/api/debrid-config', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    });
    if (!resp.ok) {
      throw new Error('Unable to save Debrid details');
    }
    await loadDebridConfig();
    closeDebridModal();
  } catch (err) {
    console.error(err);
    alert('Failed to save Debrid settings.');
  } finally {
    btn.disabled = false;
  }
}

function updateDebridQueueDisplay(status, body, items = []) {
  const statusEl = document.getElementById('debrid-queue-status');
  const bodyEl = document.getElementById('debrid-queue-body');
  const timeEl = document.getElementById('debrid-queue-time');
  if (statusEl) statusEl.textContent = status;
  if (bodyEl) bodyEl.textContent = body;
  if (timeEl) timeEl.textContent = new Date().toLocaleTimeString();
  renderDebridQueueList(items);
}

function startDebridQueueMonitor() {
  if (!debridConfig.ip || !debridConfig.username) {
    updateDebridQueueDisplay('Waiting for configuration…', 'Provide the Real Debrid IP, username, and password to begin polling.');
    return;
  }
  stopDebridQueueMonitor();
  fetchDebridQueue();
  debridQueueTimer = setInterval(fetchDebridQueue, 1000);
}

function stopDebridQueueMonitor() {
  if (debridQueueTimer) {
    clearInterval(debridQueueTimer);
    debridQueueTimer = null;
  }
}

async function fetchDebridQueue() {
  if (!debridConfig.ip || !debridConfig.username) {
    updateDebridQueueDisplay('Missing credentials', 'Set the Debrid configuration before polling the queue.');
    return;
  }
  try {
    const resp = await fetch('/api/debrid-queue', {
      cache: 'no-cache',
    });
    const payload = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      const errMessage = payload.error || payload.detail || 'Proxy error';
      throw new Error(errMessage);
    }
    let body = payload.body || '';
    if (!body && payload.json) {
      body = JSON.stringify(payload.json, null, 2);
    }
    if (!body) body = '[empty response]';
    const status = `HTTP ${payload.status_code || resp.status}`;
    let items = Array.isArray(payload.json) ? payload.json : [];
    updateDebridQueueDisplay(status, body, items);
  } catch (err) {
    updateDebridQueueDisplay('Proxy error', err?.message || 'Unable to reach endpoint');
  }
}

function renderDebridQueueList(items) {
  const container = document.getElementById('debrid-queue-list');
  if (!container) return;
  if (!items.length) {
    container.innerHTML = '<div class="debrid-queue-empty">No torrents currently queued.</div>';
    return;
  }
  container.innerHTML = items.map(item => {
    const percent = Number.isFinite(Number(item.downloadedPercent))
      ? Math.max(0, Math.min(100, Number(item.downloadedPercent)))
      : null;
    const completedFiles = Number.isFinite(Number(item.completedFilesCount))
      ? Math.max(0, Math.trunc(Number(item.completedFilesCount)))
      : null;
    const activeFiles = Number.isFinite(Number(item.activeFilesCount))
      ? Math.max(0, Math.trunc(Number(item.activeFilesCount)))
      : null;
    const totalFiles = Number.isFinite(Number(item.totalFilesToDownload))
      ? Math.max(0, Math.trunc(Number(item.totalFilesToDownload)))
      : null;
    const fileCountsLabel = `${completedFiles ?? '—'} / ${activeFiles ?? '—'} / ${totalFiles ?? '—'}`;
    const percentLabel = percent != null ? `${percent.toFixed(1)}%` : '—';
    const speed = Number.isFinite(Number(item.currentDownloadSpeedBytesPerSecond))
      ? formatBytesPerSecond(Number(item.currentDownloadSpeedBytesPerSecond))
      : '—';
    const progressWidth = percent != null ? `${percent}%` : '0%';
    const name = item.name || 'Unnamed torrent';
    return `
      <div class="debrid-queue-item">
        <div class="debrid-queue-item-header">
          <div class="debrid-queue-item-name" title="${escapeHtml(name)}">${escapeHtml(name)}</div>
          <div class="debrid-queue-item-meta">
            <div class="debrid-queue-item-meta-row">
              <span>${fileCountsLabel}</span>
            </div>
            <div class="debrid-queue-item-meta-row">
              <span>${percentLabel}</span>
              <span>${speed}</span>
            </div>
          </div>
        </div>
        <div class="debrid-progress">
          <div class="debrid-progress-fill" style="width:${progressWidth}"></div>
        </div>
      </div>`;
  }).join('');
}

// Load cached SMART data from the database on page load.
fetchLogoConfig().catch(err => console.error('Failed to load app logo', err));
loadOverview();
startHostStatsPoll();
loadDebridConfig();
setupDebridMagnetInput();
applyDebridQueueVisibility();
</script>
</body>
</html>
"""
