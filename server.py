#!/usr/bin/env python

import json
from flask import Flask, jsonify, render_template, request, make_response
from controller import Outlets, Scheduler

# Super simple web service
app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True

# Pin control
outlets = Outlets()
scheduler = Scheduler()



"""

Single outlet API

"""
@app.route('/outlets/<num>/', methods=['GET'])
def get_out(num):
  return jsonify(outlets[num].serialize())

@app.route('/outlets/<num>/', methods=['PUT'])
def set_out(num):
  pin = outlets[num]
  requestJson = json.loads(request.data)
  pin.value = int(requestJson['value'])
  outlets.save()
  return jsonify(outlets[num].serialize())



"""

Batch API

"""
@app.route('/outlets/', methods=['GET'])
def get_all():
  return jsonify(outlets.serialize())

@app.route('/outlets/', methods=['PUT'])
def set_all():
  for k, v in json.loads(request.data).iteritems():
    outlets[k].value = v['value']
  outlets.save()
  return jsonify(outlets.serialize())



"""

Cron

"""
@app.route('/schedules/', methods=['GET'])
def get_schedule():
  scheduler.refresh()
  resp = make_response(json.dumps(scheduler.jobs, indent=4))
  resp.mimetype = 'application/json'
  return resp

@app.route('/schedules/<name>/', methods=['GET'])
def get_one_schedule(name):
  scheduler.refresh()
  return jsonify(scheduler.get_job_by_name(name))  #TODO: or 404

@app.route('/schedules/<name>/', methods=['PUT'])
def set_one_schedule(name):
  job = scheduler.get_job_by_name(name)   #TODO: handle not found state
  for k, v in json.loads(request.data).iteritems():
    job[k] = v
  
  scheduler.save();
  scheduler.refresh();
  return jsonify(scheduler.get_job_by_name(job['name']))



"""

Pages

"""
@app.route('/')
def index():
  return render_template('index.html')

# Entry point
if __name__ == '__main__':
  app.run(host='0.0.0.0')
