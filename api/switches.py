import json
from flask import Blueprint, jsonify, request
from .helpers import jsonify_array

switches_api = Blueprint('switches_api', __name__, url_prefix='/api')

def init_switches_api(switches):
  @switches_api.route('/switches/', methods=['GET'])
  def get_all():
    return jsonify_array(switches.serialize())

  @switches_api.route('/switches/', methods=['PUT'])
  def set_all():
    for v in json.loads(request.data):
      if v['value'] is not None:   # null check so we can batch save schedule.switches payloads
        switches[v['name']].value = v['value']
    switches.save()
    return jsonify_array(switches.serialize())

  @switches_api.route('/switches/<num>', methods=['GET'])
  def get_one(num):
    return jsonify(switches[num].serialize())

  @switches_api.route('/switches/<num>', methods=['PUT'])
  def set_one(num):
    pin = switches[num]
    requestJson = json.loads(request.data)
    pin.value = int(requestJson['value'])
    switches.save()
    return jsonify(switches[num].serialize())

  return switches_api