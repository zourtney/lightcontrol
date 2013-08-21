#!/usr/bin/env python

import json
from flask import Flask, jsonify, render_template, request, make_response
from gpiocrust import Header, OutputPin

# Set up Raspberry Pi I/O
header = Header()
out = {
    1: OutputPin(15),
    2: OutputPin(13),
    3: OutputPin(12),
    4: OutputPin(11)
}


# Super simple web service
app = Flask(__name__, static_folder='templates', static_url_path='')
app.debug = True



"""

Single outlet API

"""
def serialize_outlet(num):
  outlet = out[int(num)]
  return {
    'id': int(num),
    'value': outlet.value
  }

@app.route('/outlets/<num>/', methods=['GET'])
def get_out(num):
  return jsonify(serialize_outlet(num))

@app.route('/outlets/<num>/', methods=['PUT'])
def set_out(num):
  pin = out[int(num)]
  requestJson = json.loads(request.data)
  pin.value = int(requestJson['value'])
  return jsonify(serialize_outlet(num))



"""

Batch API

"""
def serialize_all():
  return [
    serialize_outlet(1),
    serialize_outlet(2),
    serialize_outlet(3),
    serialize_outlet(4)
  ]

@app.route('/outlets/', methods=['GET'])
def get_all():
  resp = make_response(json.dumps(serialize_all()))
  resp.mimetype = 'application/json'
  return resp

@app.route('/outlets/', methods=['PUT'])
def set_all():
  for outlet in json.loads(request.data):
    out[int(outlet['id'])].value = outlet['value']
  resp = make_response(json.dumps(serialize_all()))
  resp.mimetype = 'application/json'
  return resp



"""

Pages

"""
@app.route('/')
def index():
  return render_template('index.html')

# Entry point
if __name__ == '__main__':
  app.run(host='0.0.0.0')
