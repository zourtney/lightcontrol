from flask import Blueprint
from .helpers import jsonify_array, proxy_get, proxy_put

zones_routes = Blueprint('zones_routes', __name__, url_prefix='/api')

def make_zones_routes(zones):
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
    return proxy_get(url=zone['address'] + '/api/version')

  # Proxy switches / outlets
  @zones_routes.route('/zones/<zone_name>/switches/', methods=['GET'])
  def proxy_get_switches(zone_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_get(url=zone['address'] + '/api/switches/',
                     fallback_url=zone['address'] + '/outlets/')  # legacy

  @zones_routes.route('/zones/<zone_name>/switches/', methods=['PUT'])
  def proxy_put_switches(zone_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_put(url=zone['address'] + '/api/switches/',
                     fallback_url=zone['address'] + '/outlets/')  # legacy

  @zones_routes.route('/zones/<zone_name>/switches/<switch_name>', methods=['GET'])
  def proxy_get_switch(zone_name, switch_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_get(url=zone['address'] + '/api/switches/' + switch_name,
                     fallback_url=zone['address'] + '/outlets/' + switch_name + '/')  # legacy

  @zones_routes.route('/zones/<zone_name>/switches/<switch_name>', methods=['PUT'])
  def proxy_put_switch(zone_name, switch_name):
    zone = get_zone(zone_name)   #TODO: return 404 for null zone
    return proxy_put(url=zone['address'] + '/api/switches/' + switch_name,
                     fallback_url=zone['address'] + '/outlets/' + switch_name + '/')  # legacy

  # Proxy schedules
  @zones_routes.route('/zones/<zone_name>/schedules/', methods=['GET'])
  def proxy_get_schedules(zone_name):
    zone = get_zone(zone_name)
    r = proxy_get(url=zone['address'] + '/api/schedules/')
    
    if r.status_code == 404:
      print 'trying legacy mode...'
      r = proxy_get(url=zone['address'] + '/schedules/')
      r.data.switches = r.data.outlets
      print r.data

    return r

  return zones_routes

