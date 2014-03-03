import json
from gpiocrust import Header, OutputPin


class Switch(OutputPin):
  """A single GPIO output pin with some metadata"""
  def __init__(self, name, pin, value=0, initial=None):
    super(Switch, self).__init__(pin, value=value)
    self._name = name
    self._initial = initial

  def serialize(self):
    return {
      'name': self._name,
      'pin': self._pin,
      'value': self.value,
      'initial': self._initial
    }


class Switches(object):
  """Manager object for a collection of switches"""
  def __init__(self, settings=None):
    self._header = Header()
    self._settings = settings
    self._switches = {}
    self._load()
    self.save()

  def _load(self):
    for s in self._settings['switches']:
      initial = s['initial'] if 'initial' in s and s['initial'] is not None else s['value']
      self._switches[s['name']] = Switch(s['name'], s['pin'], value=initial, initial=s['initial'])

  def save(self):
    self._settings['switches'] = self.serialize()
    self._settings.save();

  def serialize(self):
    return [v.serialize() for k, v in self._switches.iteritems()]

  def __getitem__(self, key):
    return self._switches[key]

  def iterkeys(self):
    return self._switches.iterkeys()

  def iteritems(self):
    return self._switches.iteritems()