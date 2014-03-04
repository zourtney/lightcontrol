#!/usr/bin/env python

import os
import sys
import requests
import json
from server import LightControl
from lightcontrol import Switches, Cli, Settings

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def main(argv):
  parser = Cli()
  args = parser.parse_args()

  # Load settings
  if args.settings:
    settings = Settings(file=args.settings)
  else:
    settings = Settings(filename=ROOT_PATH + '/settings.json')

  # Command line overrides
  if args.port:
    settings['port'] = args.port
  if args.debug:
    settings['debug'] = True
  
  if args.start:
    # Start server
    print 'Starting server on http://0.0.0.0:%s [debug=%s]' % (settings['port'], settings['debug'])
    app = LightControl(settings=settings)
    app.start()
    #TODO: set switches also? `app.start` is a blocking call :-(
  elif args.switch:
    # Set switches via HTTP (avoiding GPIO conflicts, making server "point of contact")
    url = 'http://0.0.0.0:%s/api/switches/' % settings['port']
    
    # Convert to [{'name': 'switch name', 'value': 0}, ...]
    print 'Setting switches', args.switches.keys()
    switches = [{'name': k, 'value': v} for k, v in args.switches.iteritems()]
    r = requests.put(url, json.dumps(switches))
    
    if r.status_code == 200:
      print 'Success!'
    else:
      print 'Error %s, %s' % (r.status_code, r.text)


if __name__ == '__main__':
  main(sys.argv[1:])