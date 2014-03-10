from flask import Blueprint
from .helpers import jsonify_array, proxy_request

zones_routes = Blueprint('zones_routes', __name__, url_prefix='/api')

def make_zones_routes(zones):
  """
  A fairly ugly, primative, and verbose approach to routing requests to zone
  URLs to their respective host. It works though.

  This also creates the URL definition for `/api/zones/`, which I guess is
  important too.
  """
  # Helper method
  def get_zone(zone_name):
    return next((z for z in zones if z['name'] == zone_name), None)

  # List all zones
  @zones_routes.route('/zones/', methods=['GET'])
  def get_all_zones():
    return jsonify_array(zones)

  # Proxy version
  @zones_routes.route('/zones/<zone_name>/version', methods=['GET'])
  def proxy_get_version(zone_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_request(method='get', url=zone['address'] + '/api/version')

  # Proxy switches / outlets
  @zones_routes.route('/zones/<zone_name>/switches/', methods=['GET'])
  def proxy_get_switches(zone_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_request(method='get', url=zone['address'] + '/api/switches/')

  @zones_routes.route('/zones/<zone_name>/switches/', methods=['PUT'])
  def proxy_update_switches(zone_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_request(method='put', url=zone['address'] + '/api/switches/')

  @zones_routes.route('/zones/<zone_name>/switches/<switch_name>', methods=['GET'])
  def proxy_get_switch(zone_name, switch_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_request(method='get', url=zone['address'] + '/api/switches/' + switch_name)

  @zones_routes.route('/zones/<zone_name>/switches/<switch_name>', methods=['PUT'])
  def proxy_update_switch(zone_name, switch_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_request(method='put', url=zone['address'] + '/api/switches/' + switch_name)

  # Proxy schedules
  @zones_routes.route('/zones/<zone_name>/schedules/', methods=['GET'])
  def proxy_get_schedules(zone_name):
    zone = get_zone(zone_name)
    return proxy_request(method='get', url=zone['address'] + '/api/schedules/')

  @zones_routes.route('/zones/<zone_name>/schedules/', methods=['POST'])
  def proxy_create_schedule(zone_name):
    zone = get_zone(zone_name)
    return proxy_request(method='post', url=zone['address'] + '/api/schedules/')

  @zones_routes.route('/zones/<zone_name>/schedules/<schedule_name>', methods=['GET'])
  def proxy_get_schedule(zone_name, schedule_name):
    zone = get_zone(zone_name)
    return proxy_request(method='get', url=zone['address'] + '/api/schedules/' + schedule_name)

  @zones_routes.route('/zones/<zone_name>/schedules/<schedule_name>', methods=['PUT'])
  def proxy_update_schedule(zone_name, schedule_name):
    zone = get_zone(zone_name)
    return proxy_request(method='put', url=zone['address'] + '/api/schedules/' + schedule_name)

  @zones_routes.route('/zones/<zone_name>/schedules/<schedule_name>', methods=['DELETE'])
  def proxy_delete_schedule(zone_name, schedule_name):
    zone = get_zone(zone_name)
    return proxy_request(method='delete', url=zone['address'] + '/api/schedules/' + schedule_name)

  return zones_routes

