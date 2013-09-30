import os
from crontab import CronTab
from cli import Cli
from constants import CRON_APP_ID


class Scheduler(object):
  """Manager object for outlet cron jobs"""
  def __init__(self, root_path=None):
    self._root_path = root_path
    self.refresh()

  def refresh(self):
    self._crontab = CronTab('root')
    self._cli = Cli()
    self._load()

  def _load(self):
    self._jobs = {}
    for cron in self._crontab:
      meta = cron.meta()
      i = meta.find(CRON_APP_ID)
      if i >= 0:
        name = meta[i + len(CRON_APP_ID):].strip()  # get string after CRON_APP_ID
        self._jobs[name] = {
          'name': name,
          'outlets': self._cli.get_outlets(command=str(cron.command)),
          'enabled': cron.is_enabled(),
          'next': str(cron.schedule().get_next()),
          'cron': str(cron.render_time())
        }
    return self._jobs
  
  #@property
  #def jobs(self):
  #  return self._jobs

  def __getitem__(self, key):
    return self._jobs[key]

  def __setitem__(self, key, item):
    self._jobs[key] = item

  def __delitem__(self, key):
    del self._jobs[key]

  def serialize(self):
    return [v for k, v in self._jobs.iteritems()]

  def save(self):
    # Remove old lightcontrol cron jobs
    crontab = self._crontab
    old_crons = [cron for cron in crontab if CRON_APP_ID in cron.meta()]
    while len(old_crons):
      crontab.remove(old_crons.pop())

    # Add new ones
    client_exe = '%s/client.py' % self._root_path
    for job in self._jobs.itervalues():
      exe = client_exe
      for k, v in job['outlets'].iteritems():
        if v['value'] is not None:
          exe += ' -%s %s' % (k, 't' if int(v['value']) == 0 else 'f')
      
      cron = crontab.new(command=exe, comment='%s %s' %(CRON_APP_ID, job['name']))
      cron.set_slices(job['cron'].split(' '))
      #print str(cron)
      #TODO: enabled flag
    crontab.write()
