#!/usr/bin/env python

import json
from flask import Flask, jsonify, render_template, request, make_response
from controller import Outlets



outlets = Outlets()

# Super simple web service
app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True









"""

Single outlet API

"""
@app.route('/outlets/<num>/', methods=['GET'])
def get_out(num):
  return jsonify(outlets[num].serialize())

#@app.route('/outlets/<num>/', methods=['PUT'])
#def set_out(num):
#  pin = out[int(num)]
#  requestJson = json.loads(request.data)
#  pin.value = int(requestJson['value'])
#  save_settings();
#  return jsonify(serialize_one(num))



"""

Batch API

"""
@app.route('/outlets/', methods=['GET'])
def get_all():
  resp = make_response(json.dumps(outlets.serialize()))
  resp.mimetype = 'application/json'
  return resp

#@app.route('/outlets/', methods=['PUT'])
#def set_all():
#  for outlet in json.loads(request.data):
#    out[int(outlet['id'])].value = outlet['value']
#  resp = make_response(json.dumps(serialize_all()))
#  resp.mimetype = 'application/json'
#  save_settings()
#  return resp



"""

Pages

"""
@app.route('/')
def index():
  return render_template('index.html')

# Entry point
if __name__ == '__main__':
  app.run(host='0.0.0.0')
