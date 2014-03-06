import json
from flask import Blueprint, jsonify, request
from .helpers import jsonify_array, proxy_get

schedules_routes = Blueprint('schedules_routes', __name__, url_prefix='/api')


def init_schedules_routes(scheduler):
  """
  Create a new blueprint for locally-controlled schedules

  For example:
      [GET] /api/schedules/
  """
  @schedules_routes.route('/schedules/', methods=['GET'])
  def get_schedule():
    scheduler.refresh()
    return jsonify_array(scheduler.serialize())

  @schedules_routes.route('/schedules/', methods=['POST'])
  def create_one_schedule():
    scheduler.refresh()
    data = json.loads(request.data)
    scheduler[data['name']] = data #.jobs.append(data)
    scheduler.save()
    scheduler.refresh()
    return jsonify(scheduler[data['name']])

  @schedules_routes.route('/schedules/<name>', methods=['GET'])
  def get_one_schedule(name):
    scheduler.refresh()
    return jsonify(scheduler[name])  #TODO: or 404

  @schedules_routes.route('/schedules/<name>', methods=['PUT'])
  def set_one_schedule(name):
    scheduler.refresh()
    job = scheduler[name]   #TODO: handle not found state
    for k, v in json.loads(request.data).iteritems():
      job[k] = v
    scheduler.save()
    scheduler.refresh()
    return jsonify(scheduler[job['name']])

  @schedules_routes.route('/schedules/<name>', methods=['DELETE'])
  def delete_one_schedule(name):
    job = scheduler[name]
    del scheduler[name]
    scheduler.save()
    return jsonify(job)

  return schedules_routes


def add_zone_schedules(blueprint=None, url_prefix='/', dest_url=None):
  """
  Register schedule routes on an existing blueprint for an existing zone.

  For example:
      [GET] /api/zones/Living%20Room/schedules/
  """
  @blueprint.route(url_prefix + '/schedules/', methods=['GET'])
  def get_schedule():
    return proxy_get(url=dest_url + '/api/schedules',
                     fallback_url=dest_url + '/schedules')  # legacy

  @blueprint.route(url_prefix + '/schedules/<name>', methods=['GET'])
  def get_one_schedule(name):
    return proxy_get(url=dest_url + '/api/schedules/' + name,
                     fallback_url=dest_url + '/schedules/' + name + '/')  # legacy
