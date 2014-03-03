#!/usr/bin/env python

import os
import sys
import json
from lightcontrol import Switches, Cli, Settings

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def print_message(msg, overwrite=False):
  if overwrite:
    sys.stdout.write('\r%s\n' % msg)
    sys.stdout.flush()
  else:
    sys.stdout.write('%s' % msg)
    sys.stdout.flush()


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
  
  if args.switch:
    print args.switches


  #s = dict(arg.split('=') for arg in args.switch)  # NOTE: can't have '=' in name or value!
  #print s
  #url = args.destination or 'http://localhost:5000/api/switches/'

  # Update switch data based on arguments, then PUT to server
  # data = parser.get_switches_for_command(args=args)
  # print_message('Setting switches...')
  # r = requests.put(url, json.dumps(data))
  # data = r.json()
  # print_message('Setting switches...success!', overwrite=True)


if __name__ == '__main__':
  main(sys.argv[1:])