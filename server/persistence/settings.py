import os
import json

class Settings(dict):
  def __init__(self, file=None, filename=None):
    self._filename = filename or os.path.abspath(file.name)
    self._load()

  def _load(self):
    with open(self._filename, 'r') as infile:
      self.update(json.load(infile))

  def save(self):
    with open(self._filename, 'w') as outfile:
      json.dump(self, outfile, indent=2)