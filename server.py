#!/usr/bin/env python

import os
import json
from flask import Flask, jsonify, render_template, request, make_response
from api import register_lightcontrol_api
from lightcontrol import Switches, Scheduler


# Super simple web service
app = Flask(__name__, template_folder='webapp/dist', static_folder='webapp/dist', static_url_path='')
app.debug = True


# Constants
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = ROOT_PATH + '/settings.json'


# Manager classes
switches = Switches(settings_file=SETTINGS_FILE)
scheduler = Scheduler(root_path=ROOT_PATH, switches=switches)


# LightControl API (hosted at /api)
register_lightcontrol_api(app=app, switches=switches, scheduler=scheduler)


# Webapp (hosted at root)
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0')
