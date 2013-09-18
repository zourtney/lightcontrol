import getopt
import shlex
from constants import SETTINGS_FILE

class Cli(object):
  @staticmethod
  def parse(argv):
    return getopt.getopt(argv, 'hd:0:1:2:3:', ['help', 'destination=', 'top-left=', 'bottom-left=', 'top-right=', 'bottom-right='])
    
  @staticmethod
  def build_data_from_string(command):
    return Cli.build_data_from_argv(shlex.split(command))

  @staticmethod
  def build_data_from_argv(argv):
    opts, args = Cli.parse(argv[1:])
    data = {}
    for o, a in opts:
      val = {'value': 0 if 't' in str(a).lower() else 1}
      if o == '-0' or o == '--top-left':
        data['0'] = val
      elif o == '-1' or o == '--bottom-left':
        data['1'] = val
      elif o == '-2' or o == '--top-right':
        data['2'] = val
      elif o == '-3' or o == '--bottom-right':
        data['3'] = val
    return data