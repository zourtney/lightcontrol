import copy
from crontab import CronTab
from cli import Cli, CliNamespace
from constants import CRON_APP_ID


class Scheduler(object):
  """Manager object for switch-controlling cron jobs"""
  def __init__(self, settings=None, updater_exe=None):
    self._settings = settings
    self._updater_exe = updater_exe
    self.refresh()

  def refresh(self):
    self._crontab = CronTab('root')
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
          'switches': self._parse_switches(command=cron.command),
          'enabled': cron.is_enabled(),
          'next': str(cron.schedule().get_next()),
          'cron': str(cron.slices.render())
        }
    return self._jobs

  def _parse_switches(self, command=None):
    args = Cli().parse_args(command=command)
    ret = copy.deepcopy(self._settings['switches'])
    for s in ret:
      s['value'] = args.switches[s['name']] if s['name'] in args.switches else None
    return ret

  def _generate_switches(self, switches):
    return CliNamespace.switches_to_command(switches)

  def save(self):
    # Remove old lightcontrol cron jobs
    crontab = self._crontab
    old_crons = [cron for cron in crontab if CRON_APP_ID in cron.comment]
    while len(old_crons):
      crontab.remove(old_crons.pop())

    # Add new ones
    for job in self._jobs.itervalues():
      args = CliNamespace()
      args.switches = job['switches']
      cron = crontab.new(command='%s %s' % (self._updater_exe, args.serialize()),
                         comment='%s %s' % (CRON_APP_ID, job['name']))
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