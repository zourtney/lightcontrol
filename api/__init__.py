from .version import version_api
from .switches import init_switches_api
from .schedules import init_schedules_api
from .zones import make_zones_api

# Use this to register URLs to a Flask app instance
def register_local_api(app=None, switches=None, scheduler=None):
  app.register_blueprint(init_switches_api(switches))
  app.register_blueprint(init_schedules_api(scheduler))
