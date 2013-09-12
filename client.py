#!/usr/bin/env python

import sys
import requests
import getopt
import json


def print_message(msg, overwrite=False):
  if overwrite:
    sys.stdout.write('\r%s\n' % msg)
    sys.stdout.flush()
  else:
    sys.stdout.write('%s' % msg)
    sys.stdout.flush()

def usage():
  print('Usage: %s [-<socket> <value>] [--<long_socket>=<value>]' % (sys.argv[0]))
  print(' -d, --destination         Specify the server destination. Default is http://localhost:5000/outlets/.')
  print(' -0, --top-left            Set the upper-left socket (0) value. Use "true" or "false".')
  print(' -1, --bottom-left         Set the bottom-left socket (1) value. Use "true" or "false".')
  print(' -2, --top-right           Set the top-right socket (2) value. Use "true" or "false".')
  print(' -3, --bottom-right        Set the bottom-right socket (3) value. Use "true" or "false".')
  print(' -h, --help                View usage')
  print('Sample usage:   %s -0 t --bottom-right=false' % (sys.argv[0]))


def update_switch_data(data, opts):
  for o, a in opts:
    val = 0 if 't' in str(a).lower() else 1
    if o == '-0' or o == '--top-left':
      data['1']['value'] = val
    elif o == '-1' or o == '--bottom-left':
      data['2']['value'] = val
    elif o == '-2' or o == '--top-right':
      data['3']['value'] = val
    elif o == '-3' or o == '--bottom-right':
      data['4']['value'] = val
  return data

  

def main(argv):
  try:
    url = 'http://localhost:5000/outlets/'
    opts, args = getopt.getopt(argv, 'hd:0:1:2:3:', ['help', 'destination=', 'top-left=', 'bottom-left=', 'top-right=', 'bottom-right='])

    for o, a in opts:
      if o in ('-h', '--help'):
        usage()
        sys.exit()
      elif o in ('-d', '--destination'):
      	url = a
      
    # Get the server URL
    print_message('Fetching current status...')
    r = requests.get(url)
    data = r.json()
    print_message('Fetching current status...success!', overwrite=True)

    # Update switch data based on arguments, then PUT to server
    update_switch_data(data, opts)
    print_message('Setting switches...')
    r = requests.put(url, json.dumps(data))
    data = r.json()
    print_message('Setting switches...success!', overwrite=True)
  except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(2)


if __name__ == "__main__":
  main(sys.argv[1:])