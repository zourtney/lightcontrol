#!/usr/bin/env python

import os
from flask import Flask, render_template
from api import version_api, register_local_api, make_zones_api
from lightcontrol import Settings, Switches, Scheduler

WEBAPP_DIR = 'webapp/dist'
WEBAPP_URL = ''
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


class LightControl(object):
  def __init__(self, settings=None):
    self._settings = settings
    self._init()

  def _init(self):
    server = Flask(__name__,
                   template_folder=WEBAPP_DIR,
                   static_folder=WEBAPP_DIR,
                   static_url_path=WEBAPP_URL)

    server.debug = True#settings['debug']
    server.register_blueprint(version_api)
    server.add_url_rule('/', 'webapp_index', self._show_webapp_index)
    self._server = server

    # Initialize zones
    if 'zones' in self._settings:
      api = make_zones_api(self._settings['zones'])
      server.register_blueprint(api)

    # Initialize switches and schedules
    self._switches = Switches(settings=self._settings)
    self._scheduler = Scheduler(settings=self._settings, updater_exe=ROOT_PATH + '/cli.py')
    register_local_api(app=server, switches=self._switches, scheduler=self._scheduler)

  def _show_webapp_index(self):
    return render_template('index.html')

  def start(self):
    self._server.run(host='0.0.0.0', port=self._settings['port'])


if __name__ == '__main__':
  settings = Settings(filename='settings.json')
  app = LightControl(settings=settings)
  app.start()
