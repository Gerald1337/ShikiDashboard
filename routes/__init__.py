from .debrid import SECTION_TEMPLATE as DEBRID_SECTION_TEMPLATE
from .debrid import register as register_debrid_route
from .disks import SECTION_TEMPLATE as DISKS_SECTION_TEMPLATE
from .disks import register as register_disks_route
from .hosts import SECTION_TEMPLATE as HOSTS_SECTION_TEMPLATE
from .hosts import register as register_hosts_route
from .overview import SECTION_TEMPLATE as OVERVIEW_SECTION_TEMPLATE
from .overview import register as register_overview_route
from .services import SECTION_TEMPLATE as SERVICES_SECTION_TEMPLATE
from .services import register as register_services_route


def register_screen_routes(app, render_dashboard):
    register_overview_route(app, render_dashboard)
    register_services_route(app, render_dashboard)
    register_hosts_route(app, render_dashboard)
    register_disks_route(app, render_dashboard)
    register_debrid_route(app, render_dashboard)
