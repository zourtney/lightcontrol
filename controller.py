import json
from gpiocrust import Header, OutputPin

SETTINGS_FILE = 'settings.json'

class Outlet(OutputPin):
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
