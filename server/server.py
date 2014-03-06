import os
import json
import requests
from flask import Flask, render_template
from routes import version_routes, register_local_routes, make_zones_routes
from persistence import Settings, Switches, Scheduler, Cli

WEBAPP_DIR = 'webapp/dist'
WEBAPP_URL = ''


class LightControl(object):
  def __init__(self, root_path=None):
    self._root_path = root_path
    self._init_settings()
    self._init_http_server()

  def _init_settings(self):
    args = Cli().parse_args()
    if args.settings:
      settings = Settings(file=args.settings)
    else:
      settings = Settings(filename=self._root_path + '/settings.json')

    # Merge in defined switch values
    if args.switches:
      for s in settings['switches']:
        if s['name'] in args.switches:
          s['value'] = args.switches[s['name']]

    # Misc
    if args.port:
      settings['port'] = args.port
    if args.debug:
      settings['debug'] = True

    self._args = args
    self._settings = settings

  def _init_http_server(self):
    webapp_dir = '%s/%s' % (self._root_path, WEBAPP_DIR)
    server = Flask(__name__,
                   template_folder=webapp_dir,
                   static_folder=webapp_dir,
                   static_url_path=WEBAPP_URL)

    server.debug = self._settings['debug']
    server.register_blueprint(version_routes)
    server.add_url_rule('/', 'webapp_index', self._show_webapp_index)
    self._server = server

    # Initialize zones
    if 'zones' in self._settings:
      routes = make_zones_routes(self._settings['zones'])
      server.register_blueprint(routes)

    # Initialize switches and schedules
    self._switches = Switches(settings=self._settings)
    self._scheduler = Scheduler(settings=self._settings, updater_exe=self._root_path + '/lightcontrol.py')
    register_local_routes(app=server, switches=self._switches, scheduler=self._scheduler)

  def _show_webapp_index(self):
    return render_template('index.html')

  def start(self):
    self._server.run(host='0.0.0.0', port=self._settings['port'])

  def set_switches(self):
    url = 'http://0.0.0.0:%s/api/switches/' % self._settings['port']
    return requests.put(url, json.dumps(self._settings['switches']))

  @property
  def args(self):
    return self._args

  @property
  def settings(self):
    return self._settings
  