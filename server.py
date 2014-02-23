#!/usr/bin/env python

import os
import json
from flask import Flask, jsonify, render_template, request, make_response
from lightcontrol import Outlets, Scheduler

version = {
  'major': '1',
  'minor': '3',
  'patch': '0'
}

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = ROOT_PATH + '/settings.json'

# Super simple web service
app = Flask(__name__, template_folder='webapp/app', static_folder='webapp/app', static_url_path='')
app.debug = True

# Pin control
outlets = Outlets(settings_file=SETTINGS_FILE)
scheduler = Scheduler(root_path=ROOT_PATH, outlets=outlets)


"""

Helpers

"""
def jsonify_array(serialized_array):
  resp = make_response(json.dumps(serialized_array, indent=4))
  resp.mimetype = 'application/json'
  return resp


"""

Version controller

"""
@app.route('/version/', methods=['GET'])
@app.route('/api/version', methods=['GET'])
def get_version():
  return jsonify(version)



"""

Outlets controller

"""
@app.route('/outlets/', methods=['GET'])
@app.route('/api/outlets/', methods=['GET'])
def get_all():
  return jsonify_array(outlets.serialize())

@app.route('/outlets/', methods=['PUT'])
@app.route('/api/outlets/', methods=['PUT'])
def set_all():
  for v in json.loads(request.data):
    outlets[v['id']].value = v['value']
  outlets.save()
  return jsonify_array(outlets.serialize())

@app.route('/outlets/<num>/', methods=['GET'])
@app.route('/api/outlets/<num>', methods=['GET'])
def get_out(num):
  return jsonify(outlets[num].serialize())

@app.route('/outlets/<num>/', methods=['PUT'])
@app.route('/api/outlets/<num>', methods=['PUT'])
def set_out(num):
  pin = outlets[num]
  requestJson = json.loads(request.data)
  pin.value = int(requestJson['value'])
  outlets.save()
  return jsonify(outlets[num].serialize())



"""

Schedules controller

"""
@app.route('/schedules/', methods=['GET'])
@app.route('/api/schedules/', methods=['GET'])
def get_schedule():
  scheduler.refresh()
  return jsonify_array(scheduler.serialize())

@app.route('/schedules/', methods=['POST'])
@app.route('/api/schedules/', methods=['POST'])
def create_one_schedule():
  scheduler.refresh()
  data = json.loads(request.data)
  scheduler[data['name']] = data #.jobs.append(data)
  scheduler.save()
  scheduler.refresh()
  return jsonify(scheduler[data['name']])

@app.route('/schedules/<name>/', methods=['GET'])
@app.route('/api/schedules/<name>', methods=['GET'])
def get_one_schedule(name):
  scheduler.refresh()
  return jsonify(scheduler[name])  #TODO: or 404

@app.route('/schedules/<name>/', methods=['PUT'])
@app.route('/api/schedules/<name>', methods=['PUT'])
def set_one_schedule(name):
  scheduler.refresh()
  job = scheduler[name]   #TODO: handle not found state
  for k, v in json.loads(request.data).iteritems():
    job[k] = v
  scheduler.save()
  scheduler.refresh()
  return jsonify(scheduler[job['name']])

@app.route('/schedules/<name>/', methods=['DELETE'])
@app.route('/api/schedules/<name>', methods=['DELETE'])
def delete_one_schedule(name):
  job = scheduler[name]
  del scheduler[name]
  scheduler.save()
  return jsonify(job)



"""

Pages

"""
@app.route('/')
def index():
  return render_template('index.html')

# Entry point
if __name__ == '__main__':
  app.run(host='0.0.0.0')
