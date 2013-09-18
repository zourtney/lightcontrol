import os
from crontab import CronTab

from cli import Cli
from constants import CRON_APP_ID


class Scheduler(object):
  """Manager object for outlet cron jobs"""
  def __init__(self):
    self.refresh()

  def refresh(self):
    self._crontab = CronTab('root')
    self._get_jobs()

  def _get_jobs(self):
    self._jobs = []
    for cron in self._crontab:
      meta = cron.meta()
      i = meta.find(CRON_APP_ID)
      if i >= 0:
        self._jobs.append({
          'name': meta[i + len(CRON_APP_ID):].strip(),  # get string after CRON_APP_ID
          'outlets': Cli.build_data_from_string(str(cron.command)),
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


