import os
from crontab import CronTab
from cli import Cli
from constants import CRON_APP_ID


class Scheduler(object):
  """Manager object for switch-controlling cron jobs"""
  def __init__(self, root_path=None, switches=None):
    self._root_path = root_path
    self._switches = switches
    self.refresh()

  def refresh(self):
    self._crontab = CronTab('root')
    self._cli = Cli(switches=self._switches)
    self._load()

  def _load(self):
    self._jobs = {}
    for cron in self._crontab:
      comment = cron.comment
      i = comment.find(CRON_APP_ID)
      if i >= 0:
        name = comment[i + len(CRON_APP_ID):].strip()  # get string after CRON_APP_ID
        self._jobs[name] = {
          'name': name,
          'switches': self._cli.get_switches_for_command(command=str(cron.command)),
          'enabled': cron.is_enabled(),
          'next': str(cron.schedule().get_next()),
          'cron': str(cron.slices.render())
        }
    return self._jobs

  def save(self):
    # Remove old lightcontrol cron jobs
    crontab = self._crontab
    old_crons = [cron for cron in crontab if CRON_APP_ID in cron.comment]
    while len(old_crons):
      crontab.remove(old_crons.pop())

    # Add new ones
    client_exe = '%s/cli.py' % self._root_path
    for job in self._jobs.itervalues():
      exe = client_exe
      for s in job['switches']:
        if s['value'] is not None:
          exe += ' -"%s" %s' % (s['name'], 't' if int(s['value']) == 0 else 'f')
      
      cron = crontab.new(command=exe, comment='%s %s' %(CRON_APP_ID, job['name']))
      cron.setall(job['cron'])
      #TODO: enabled flag?
    crontab.write()
  
  def serialize(self):
    return [v for k, v in self._jobs.iteritems()]

  def __getitem__(self, key):
    return self._jobs[key]

  def __setitem__(self, key, item):
    self._jobs[key] = item

  def __delitem__(self, key):
    del self._jobs[key]