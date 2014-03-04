import os
import getopt
import shlex
import argparse


class CliNamespace(argparse.Namespace):
  def __init__(self, *args, **kwargs):
    super(CliNamespace, self).__init__(*args, **kwargs)

  def serialize(self):
    ret = ''
    if hasattr(self, 'start'):
      ret += ' start'
    if hasattr(self, 'debug') and self.debug:
      ret += ' -d'
    if hasattr(self, 'settings') and self.settings is not None:
      ret += ' --settings ' + os.path.abspath(self.settings.name)
    if hasattr(self, 'port') and self.port is not None:
      ret += ' -p ' + self.port
    if hasattr(self, 'switches') and self.switches is not None:
      for s in self.switches:
        if s['value'] is not None:
          ret += ' -s "%s"=%s' % (s['name'], int(s['value']))
    return ret

  @staticmethod
  def parse_switches(command_array=None):
    ret = {}
    if command_array is not None:
      for s in command_array:
        params = s.split('=')
        if len(params) == 2:
          ret[params[0]] = int(params[1])
    return ret


class Cli(argparse.ArgumentParser):
  def __init__(self, *args, **kwargs):
    super(Cli, self).__init__(*args, **kwargs)
    self._add_args()

  def _add_args(self):
    self.add_argument('start', nargs='?', help='starts the server')
    self.add_argument('-d', '--debug', dest='debug', action='store_true', help='run in debug mode')
    self.add_argument('--settings', type=argparse.FileType('r'), help='specify settings file location')  # http://stackoverflow.com/questions/7625786/type-dict-in-argparse-add-argument
    self.add_argument('-p', '--port', help='specify HTTP server port (other than the one provided in the settings file)')
    self.add_argument('-s', '--switch', nargs='?', help='set switch using "name=value"', action='append')

  def parse_args(self, command=None, *args, **kwargs):
    namespace = CliNamespace()
    if command:
      args = super(Cli, self).parse_args(shlex.split(command)[1:], namespace=namespace)
    else:
      args = super(Cli, self).parse_args(namespace=namespace, *args, **kwargs)
    
    # Split out "name=0" into {'name': 0}
    args.switches = CliNamespace.parse_switches(command_array=args.switch)
    return args

  def serialize_args(self):
    ret = ''
    ret += CliNamespace.serialize_switches(switch_array=self.switches)
    return ret
