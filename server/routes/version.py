from flask import Blueprint, jsonify

version_routes = Blueprint('version_routes', __name__, url_prefix='/api')

#TODO: centralize
version = {
  'major': '2',
  'minor': '0',
  'patch': '0'
}

@version_routes.route('/version', methods=['GET'])
def get_version():
  return jsonify(version)