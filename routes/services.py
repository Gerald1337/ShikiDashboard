SECTION_TEMPLATE = """
    <div class="section{% if initial_section == 'services' %} active{% endif %}" id="section-services">
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
"""


def register(app, render_dashboard):
    @app.route("/services")
    def services():
        return render_dashboard("services")
