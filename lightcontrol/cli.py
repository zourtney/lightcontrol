import os
import getopt
import shlex
import argparse
import copy


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = ROOT_PATH + '/settings.json'


class Cli(argparse.ArgumentParser):
  def __init__(self, *args, **kwargs):
    super(Cli, self).__init__(*args, **kwargs)
    self._add_arguments()

  def _add_arguments(self):
    self.add_argument('start', nargs='?', help='starts the server')
    self.add_argument('--settings', default=SETTINGS_FILE, help='specify settings file location')  # http://stackoverflow.com/questions/7625786/type-dict-in-argparse-add-argument
    self.add_argument('-s', '--switch', nargs='?', help='set switch using "name=value"', action='append')

  @property
  def switches(self):
      return self.switches
  @switches.setter
  def switches(self, value):
      self.switches = value
  

  def get_switches_for_command(self, args=None, command=None):
    if args is None:
      args = self.parse_command(command)
    args = vars(args)

    data = self._switches.serialize();
    for s in data:
      s['value'] = None if args[s['name']] is None else (0 if args[s['name']].lower() == 't' else 1)
    return data
