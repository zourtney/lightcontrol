import json
import requests
from flask import make_response, Response

def jsonify_array(serialized_array):
  resp = make_response(json.dumps(serialized_array, indent=2))
  resp.mimetype = 'application/json'
  return resp

def proxy_get(url=None, fallback_url=None):
  r = requests.get(url)

  if fallback_url is not None and r.status_code == 404:
    r = requests.get(fallback_url)
  
  return Response(
    r.text,
    status=r.status_code,
    content_type=r.headers['content-type'],
  )