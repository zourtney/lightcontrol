from flask import Blueprint, jsonify

version_api = Blueprint('version_api', __name__, url_prefix='/api')

#TODO: centralize
version = {
  'major': '1',
  'minor': '3',
  'patch': '0'
}

@version_api.route('/version', methods=['GET'])
def get_version():
  return jsonify(version)