#!/usr/bin/env python

import os
from server import LightControl

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def main():
  app = LightControl(root_path=ROOT_PATH)

  if app.args.start.lower() == 'start':
    print 'Starting server on http://0.0.0.0:%s [debug=%s]' % (app.settings['port'], app.settings['debug'])
    app.start()
  elif app.args.switch:
    try:
      r = app.set_switches()
      if r.status_code == 200:
        print 'Success!'
      else:
        print 'Error %s, %s' % (r.status_code, r.text)
    except Exception, e:
      print 'Error. Please make sure the server is running.'
      print e
  else:
    print 'Unknown option. Type "./lightcontrol.py --help" for options.'


if __name__ == '__main__':
  main()