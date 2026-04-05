SECTION_TEMPLATE = """
    <div class="section{% if initial_section == 'debrid' %} active{% endif %}" id="section-debrid">
      <div class="section-header debrid-header">
        <div>
          <div class="section-title">Debrid Client</div>
          <div class="section-subtitle small-muted" id="debrid-status">Not configured</div>
        </div>
        <div class="debrid-magnet-area">
          <input autocomplete="off" class="form-input debrid-magnet-input" id="debrid-magnet-input" type="text" placeholder="Magnet Link"/>
        </div>
        <div class="section-actions">
          <button class="icon-btn" type="button" id="debrid-queue-toggle-btn" title="Show queue panel" aria-label="Show queue panel" onclick="toggleDebridQueueVisibility()">
            <span class="material-icons" id="debrid-queue-toggle-icon">expand_more</span>
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
      <div class="debrid-queue-wrapper hidden" id="debrid-queue-wrapper">
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
"""


def register(app, render_dashboard):
    @app.route("/debrid")
    def debrid():
        return render_dashboard("debrid")
