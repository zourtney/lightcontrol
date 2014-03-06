from flask import Blueprint
from .helpers import jsonify_array
from .schedules import add_zone_schedules

zones_routes = Blueprint('zones_routes', __name__, url_prefix='/api/zones')

def make_zones_routes(zones):
  @zones_routes.route('/', methods=['GET'])
  def get_all_zones():
    return jsonify_array(zones)

  # Proxy routes from zone nodes to '/api/zones/<name>/<whatever>'
  for zone in zones:
    add_zone_schedules(blueprint=zones_routes,
                       url_prefix='/' + zone['name'],
                       dest_url='http://' + zone['address'])

  return zones_routes