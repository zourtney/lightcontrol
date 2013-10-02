import getopt
import shlex
import argparse
import copy


class Cli(argparse.ArgumentParser):
  def __init__(self, *args, **kwargs):
    super(Cli, self).__init__(*args, **kwargs)
    self._add_arguments()

  def _add_arguments(self):
    self.add_argument('-d', '--destination', help='Destination server path. Default is http://localhost:5000/outlets/')
    self.add_argument('-0', '--0', metavar='t|f', help='Socket #0 state. Use "t" or "f"')
    self.add_argument('-1', '--1', metavar='t|f', help='Socket #1 state. Use "t" or "f"')
    self.add_argument('-2', '--2', metavar='t|f', help='Socket #2 state. Use "t" or "f"')
    self.add_argument('-3', '--3', metavar='t|f', help='Socket #3 state. Use "t" or "f"')

  def parse_command(self, command):
    return self.parse_args(shlex.split(command)[1:])  # parse everything except the first item, the executable

  def get_outlets(self, args=None, command=None, switch_data=[]):
    if args is None:
      args = self.parse_command(command)

    data = copy.deepcopy(switch_data)
    for k, v in vars(args).iteritems():
      if v is not None and k in ['0', '1', '2', '3']:
        val = 0 if v.lower() == 't' else 1
        data.append({'id': k, 'value': val})
    return data
