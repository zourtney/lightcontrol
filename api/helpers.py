import json
from flask import make_response

def jsonify_array(serialized_array):
  resp = make_response(json.dumps(serialized_array, indent=4))
  resp.mimetype = 'application/json'
  return resp
