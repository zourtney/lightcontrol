import unittest
from lightcontrol.routes.helpers import jsonify_array, proxy_request


def test_jsonify_array_exists():
  assert jsonify_array

def test_proxy_request_exists():
  assert proxy_request