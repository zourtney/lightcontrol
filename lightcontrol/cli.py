import getopt
import shlex
import argparse
import copy


class Cli(argparse.ArgumentParser):
  def __init__(self, switches=None, *args, **kwargs):
    super(Cli, self).__init__(*args, **kwargs)
    self._switches = switches
    self._add_arguments()

  def _add_arguments(self):
    self.add_argument('-d', '--destination', help='Destination server path. Default is http://localhost:5000/api/switches/')
    for k in self._switches.iterkeys():
      self.add_argument('-' + k, metavar='t|f', help='Set value for ' + k + '. Use "t" or "f".')

  def parse_command(self, command):
    return self.parse_args(shlex.split(command)[1:])  # parse everything except the first item, the executable

  def get_switches(self, args=None, command=None):
    if args is None:
      args = self.parse_command(command)
    args = vars(args)

    data = self._switches.serialize();
    for s in data:
      s['value'] = None if args[s['name']] is None else (0 if args[s['name']].lower() == 't' else 1)
    return data
