import json
from flask import Blueprint, jsonify, request
from .helpers import jsonify_array

schedules_api = Blueprint('schedules_api', __name__, url_prefix='/api')

def init_schedules_api(scheduler):
  @schedules_api.route('/schedules/', methods=['GET'])
  def get_schedule():
    scheduler.refresh()
    return jsonify_array(scheduler.serialize())

  @schedules_api.route('/schedules/', methods=['POST'])
  def create_one_schedule():
    scheduler.refresh()
    data = json.loads(request.data)
    scheduler[data['name']] = data #.jobs.append(data)
    scheduler.save()
    scheduler.refresh()
    return jsonify(scheduler[data['name']])

  @schedules_api.route('/schedules/<name>', methods=['GET'])
  def get_one_schedule(name):
    scheduler.refresh()
    return jsonify(scheduler[name])  #TODO: or 404

  @schedules_api.route('/schedules/<name>', methods=['PUT'])
  def set_one_schedule(name):
    scheduler.refresh()
    job = scheduler[name]   #TODO: handle not found state
    for k, v in json.loads(request.data).iteritems():
      job[k] = v
    scheduler.save()
    scheduler.refresh()
    return jsonify(scheduler[job['name']])

  @schedules_api.route('/schedules/<name>', methods=['DELETE'])
  def delete_one_schedule(name):
    job = scheduler[name]
    del scheduler[name]
    scheduler.save()
    return jsonify(job)

  return schedules_api
