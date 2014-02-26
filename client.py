#!/usr/bin/env python

import os
import sys
import requests
import json
from lightcontrol import Switches, Cli

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = ROOT_PATH + '/settings.json'


def print_message(msg, overwrite=False):
  if overwrite:
    sys.stdout.write('\r%s\n' % msg)
    sys.stdout.flush()
  else:
    sys.stdout.write('%s' % msg)
    sys.stdout.flush()


def main(argv):
  switches = Switches(settings_file=SETTINGS_FILE)
  parser = Cli(switches=switches)
  args = parser.parse_args()
  url = args.destination or 'http://localhost:5000/api/switches/'

  # Update switch data based on arguments, then PUT to server
  data = parser.get_switches_for_command(args=args)
  print_message('Setting switches...')
  r = requests.put(url, json.dumps(data))
  data = r.json()
  print_message('Setting switches...success!', overwrite=True)


if __name__ == '__main__':
  main(sys.argv[1:])