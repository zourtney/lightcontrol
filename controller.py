import json
from gpiocrust import Header, OutputPin
from crontab import CronTab
import getopt
import shlex

SETTINGS_FILE = 'settings.json'

class Scheduler(object):
  """Manager object for outlet cron jobs"""
  def __init__(self):
    self._cron = CronTab('root')

  def _get_outlets_for_job(self, job):
    argv = shlex.split(str(job.command))
    opts, args = getopt.getopt(argv[1:], 'hd:0:1:2:3:', ['help', 'destination=', 'top-left=', 'bottom-left=', 'top-right=', 'bottom-right='])
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

  @property
  def jobs(self):
    jobs = []
    for job in self._cron.find_command('client.py'):
      jobs.append({
        'outlets': self._get_outlets_for_job(job),
        'enabled': job.is_enabled(),
        'next': str(job.schedule().get_next()),
        'cron': str(job.render_time())
      })
    return jobs



class Outlet(OutputPin):
  """A single output pin"""
  def __init__(self, id, pin, value=0, initial=None):
    super(Outlet, self).__init__(pin, value=value)
    self._id = id
    self._initial = initial

  def serialize(self):
    return {
      'id': self._id,
      'pin': self._pin,
      'value': self.value,
      'initial': self._initial
    }



class Outlets(object):
  """Manager object for a collection of outlets"""
  def __init__(self, settings_file=SETTINGS_FILE):
    self._header = Header()
    self._settings_filename = settings_file
    self._load()
    self.save()

  def _load(self):
    with open(self._settings_filename, 'r') as infile:
      opts = json.load(infile)
      self._pins = {}
      for i, p in opts['pins'].iteritems():
        initial = p['initial'] if 'initial' in p and p['initial'] is not None else p['value']
        self._pins[i] = Outlet(i, p['pin'], value=initial, initial=p['initial'])

  def save(self):
    with open(self._settings_filename, 'w') as outfile:
      obj = {
        'pins': self.serialize()
      }
      json.dump(obj, outfile, indent=4)

  def serialize(self):
    ret = {}
    for i in self._pins.keys():
      ret[i] = self._pins[i].serialize()
    return ret

  def __getitem__(self, key):
    return self._pins[key]
