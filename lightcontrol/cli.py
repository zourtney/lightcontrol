import getopt
import shlex
import argparse
import copy


class Cli(argparse.ArgumentParser):
  def __init__(self, outlets=None, *args, **kwargs):
    super(Cli, self).__init__(*args, **kwargs)
    self._outlets = outlets
    self._add_arguments()

  def _add_arguments(self):
    self.add_argument('-d', '--destination', help='Destination server path. Default is http://localhost:5000/outlets/')
    for k in self._outlets.iterkeys():
      self.add_argument('-' + k, metavar='t|f', help='Set value for ' + k + '. Use "t" or "f".')

  def parse_command(self, command):
    return self.parse_args(shlex.split(command)[1:])  # parse everything except the first item, the executable

  def get_outlets(self, args=None, command=None):
    if args is None:
      args = self.parse_command(command)
    args = vars(args)

    data = self._outlets.serialize();
    for outlet in data:
      outlet['value'] = None if args[outlet['id']] is None else (0 if args[outlet['id']].lower() == 't' else 1)
    return data
