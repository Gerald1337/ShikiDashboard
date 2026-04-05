SECTION_TEMPLATE = """
    <div class="section{% if initial_section == 'overview' %} active{% endif %}" id="section-overview">
      <div class="overview-grid">
{{ overview_widgets|safe }}
      </div>
    </div>
"""


def register(app, render_dashboard):
    @app.route("/")
    @app.route("/overview")
    def overview():
        return render_dashboard("overview")
