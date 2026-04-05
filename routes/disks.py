SECTION_TEMPLATE = """
    <div class="section{% if initial_section == 'disks' %} active{% endif %}" id="section-disks">
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
"""


def register(app, render_dashboard):
    @app.route("/disks")
    def disks():
        return render_dashboard("disks")
