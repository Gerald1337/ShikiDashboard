SECTION_TEMPLATE = """
    <div class="section{% if initial_section == 'hosts' %} active{% endif %}" id="section-hosts">
      <div class="section-header">
        <div>
          <div class="section-title">Hosts</div>
          <div class="section-subtitle small-muted">Remote machine resource monitoring with 1-minute charts and 1-hour retention.</div>
        </div>
        <div class="section-actions">
          <button class="icon-btn" type="button" title="Add Host" aria-label="Add Host" onclick="openHostModal()">
            <span class="material-icons">add</span>
          </button>
          <button class="icon-btn" type="button" title="Reorder hosts" onclick="openReorderModal('hosts')">
            <span class="material-icons">settings</span>
          </button>
        </div>
      </div>
      <div id="hosts-container">
        <div class="loading"><div class="loading-spinner"></div>Loading…</div>
      </div>
    </div>
"""


def register(app, render_dashboard):
    @app.route("/hosts")
    def hosts():
        return render_dashboard("hosts")
