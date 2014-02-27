#!/usr/bin/env python

import os
from flask import Flask, render_template
from api import version_api, register_local_api, make_zones_api
from lightcontrol import Settings, Switches, Scheduler


# Load settings
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = ROOT_PATH + '/settings.json'
settings = Settings(filename=SETTINGS_FILE)
debug = 'debug' in settings and settings['debug'] == True


# Super simple web service
app = Flask(__name__, template_folder='webapp/dist', static_folder='webapp/dist', static_url_path='')
app.debug = debug


# Register version API
app.register_blueprint(version_api)


# Initialize zones, if any
if 'zones' in settings:
  api = make_zones_api(settings['zones'])
  app.register_blueprint(api)


# Initialize local GPIO pins, if any
# if 'switches' in settings:
#   # Manager classes
#   switches = Switches(settings_file=SETTINGS_FILE)
#   scheduler = Scheduler(root_path=ROOT_PATH, switches=switches)
#   register_local_api(app=app, switches=switches, scheduler=scheduler)



# Webapp (hosted at root)
@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  port = settings['port'] if 'port' in settings else None
  app.run(host='0.0.0.0', port=port)
