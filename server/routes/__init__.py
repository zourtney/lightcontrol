from .version import version_routes
from .switches import init_switches_routes
from .schedules import init_schedules_routes
from .zones import make_zones_routes

# Use this to register URLs to a Flask app instance
def register_local_routes(app=None, switches=None, scheduler=None):
  app.register_blueprint(init_switches_routes(switches))
  app.register_blueprint(init_schedules_routes(scheduler))
