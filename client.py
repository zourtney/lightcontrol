#!/usr/bin/env python

import sys
import requests
import json
from lightcontrol import Cli


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
  url = args.destination or 'http://localhost:5000/outlets/'

  # Get the current dataset.
  print_message('Fetching current status...')
  r = requests.get(url)
  data = r.json()
  print_message('Fetching current status...success!', overwrite=True)

  # Update switch data based on arguments, then PUT to server
  data = parser.get_outlets(args=args, switch_data=data)
  print_message('Setting switches...')
  r = requests.put(url, json.dumps(data))
  data = r.json()
  print_message('Setting switches...success!', overwrite=True)


if __name__ == "__main__":
  main(sys.argv[1:])