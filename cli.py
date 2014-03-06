#!/usr/bin/env python

import os
import sys
import requests
import json
from server import LightControl
from lightcontrol import Switches, Cli, Settings

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def create_settings(args=None):
  """Create settings object, merging in command line arguments"""
  if args.settings:
    settings = Settings(file=args.settings)
  else:
    settings = Settings(filename=ROOT_PATH + '/settings.json')

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

  return settings


def start_server(settings=None):
  """Start the HTTP server"""
  app = LightControl(settings=settings)
  app.start()


def main():
  parser = Cli()
  args = parser.parse_args()
  settings = create_settings(args=args)

  if args.start:
    # Start server
    print 'Starting server on http://0.0.0.0:%s [debug=%s]' % (settings['port'], settings['debug'])
    start_server(settings=settings)
  elif args.switch:
    # Set switches via HTTP (avoiding GPIO conflicts, making server "point of contact")
    url = 'http://0.0.0.0:%s/api/switches/' % settings['port']
    try:
      print 'Setting switches...'
      r = requests.put(url, json.dumps(settings['switches']))   # we can get away with setting everything...
      if r.status_code == 200:
        print 'Success!'
      else:
        print 'Error %s, %s' % (r.status_code, r.text)
    except Exception, e:
      print 'Error. Please make sure the server is running.'
      print e


if __name__ == '__main__':
  main()