import json
import requests
from flask import make_response, Response, request

"""

JSON serialization

"""
def jsonify_array(serialized_array):
  resp = make_response(json.dumps(serialized_array, indent=2))
  resp.mimetype = 'application/json'
  return resp


"""

HTTP proxying methods. Very primititve.

"""
def proxy_request(url=None, method=None):
  fn = getattr(requests, method)   # handle to requests.get, requests.put, etc
  r = fn(url=url, data=request.data)
  return Response(
    r.text,
    status=r.status_code,
    content_type=r.headers['content-type']
  )