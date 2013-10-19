import json
from gpiocrust import Header, OutputPin


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
  def __init__(self, settings_file=None):
    self._header = Header()
    self._settings_filename = settings_file
    self._load()
    self.save()

  def _load(self):
    with open(self._settings_filename, 'r') as infile:
      opts = json.load(infile)
      self._pins = {}
      for p in opts['pins']:
        initial = p['initial'] if 'initial' in p and p['initial'] is not None else p['value']
        self._pins[p['id']] = Outlet(p['id'], p['pin'], value=initial, initial=p['initial'])

  def save(self):
    with open(self._settings_filename, 'w') as outfile:
      obj = {
        'pins': self.serialize()
      }
      json.dump(obj, outfile, indent=4)

  def serialize(self):
    return [v.serialize() for k, v in self._pins.iteritems()]

  def __getitem__(self, key):
    return self._pins[key]