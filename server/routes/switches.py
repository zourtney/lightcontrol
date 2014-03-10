import json
from flask import Blueprint, jsonify, request
from .helpers import jsonify_array

switches_routes = Blueprint('switches_routes', __name__, url_prefix='/api')

def init_switches_routes(switches):
  """
  Create a new blueprint for locally-controlled switches

  For example:
      [GET] /api/switches/
  """
  @switches_routes.route('/switches/', methods=['GET'])
  def get_all():
    return jsonify_array(switches.serialize())

  @switches_routes.route('/switches/', methods=['PUT'])
  def set_all():
    for v in json.loads(request.data):
      if v['value'] is not None:   # null check so we can batch save schedule.switches payloads
        switches[v['name']].value = v['value']
    switches.save()
    return jsonify_array(switches.serialize())

  @switches_routes.route('/switches/<num>', methods=['GET'])
  def get_one(num):
    return jsonify(switches[num].serialize())

  @switches_routes.route('/switches/<num>', methods=['PUT'])
  def set_one(num):
    pin = switches[num]
    requestJson = json.loads(request.data)
    pin.value = int(requestJson['value'])
    switches.save()
    return jsonify(switches[num].serialize())

  return switches_routes
