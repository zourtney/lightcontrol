#!/usr/bin/env python

import json
from flask import Flask, jsonify, render_template, request, make_response
from controller import Outlets

# Super simple web service
app = Flask(__name__, static_folder='static', static_url_path='')
app.debug = True

# Pin control
outlets = Outlets()



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

Pages

"""
@app.route('/')
def index():
  return render_template('index.html')

# Entry point
if __name__ == '__main__':
  app.run(host='0.0.0.0')
