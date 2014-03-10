import json
from flask import Blueprint, jsonify, request
from .helpers import jsonify_array

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