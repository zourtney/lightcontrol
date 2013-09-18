import os
import json
from gpiocrust import Header, OutputPin
from crontab import CronTab
import getopt
import shlex

SETTINGS_FILE = 'settings.json'
CRON_APP_ID = 'lightcontrol'

class Scheduler(object):
  def __init__(self):
    self.refresh()

  def refresh(self):
    self._crontab = CronTab('root')
    self._get_jobs()

  """Manager object for outlet cron jobs"""
  def _get_outlets_for_cron(self, job):
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

  def _get_jobs(self):
    self._jobs = []
    for cron in self._crontab:
      meta = cron.meta()
      i = meta.find(CRON_APP_ID)
      if i >= 0:
        self._jobs.append({
          'name': meta[i + len(CRON_APP_ID):].strip(),
          'outlets': self._get_outlets_for_cron(cron),
          'enabled': cron.is_enabled(),
          'next': str(cron.schedule().get_next()),
          'cron': str(cron.render_time())
        })
    return self._jobs
  
  @property
  def jobs(self):
    return self._jobs

  def get_job_by_name(self, name):
    for job in self._jobs:
      if job['name'] == name:
        return job
    return None

  def save(self):
    # Remove old lightcontrol cron jobs
    crontab = self._crontab
    old_crons = [cron for cron in crontab if CRON_APP_ID in cron.meta()]
    while len(old_crons):
      crontab.remove(old_crons.pop())

    # Add new ones
    client_exe = '%s/client.py' % os.path.dirname(os.path.realpath(__file__)) 
    for job in self._jobs:
      exe = client_exe
      for k, v in job['outlets'].iteritems():
        if v['value'] is not None:
          exe += ' -%s %s' % (k, 't' if int(v['value']) == 0 else 'f')
      
      cron = crontab.new(command=exe, comment='%s %s' %(CRON_APP_ID, job['name']))
      cron.set_slices(job['cron'].split(' '))
      print str(cron)
      #TODO: enabled flag
    crontab.write()


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
