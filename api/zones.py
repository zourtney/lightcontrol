from flask import Blueprint
from .helpers import jsonify_array
from .schedules import add_zone_schedules

zones_api = Blueprint('zones_api', __name__, url_prefix='/api/zones')

def make_zones_api(zones):
  @zones_api.route('/', methods=['GET'])
  def get_all_zones():
    return jsonify_array(zones)

  # Proxy routes from zone nodes to '/api/zones/<name>/<whatever>'
  for zone in zones:
    add_zone_schedules(blueprint=zones_api,
                       url_prefix='/' + zone['name'],
                       dest_url='http://' + zone['address'])

  return zones_api