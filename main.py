#import copy
#from time import sleep
import json
from flask import Flask, jsonify, render_template, request
from gpiocrust import Header, OutputPin#, PWMOutputPin, InputPin

# Set up Raspberry Pi I/O
header = Header()
out = {
    1: OutputPin(15),
    2: OutputPin(13),
    3: OutputPin(12),
    4: OutputPin(11)
}


# Super simple web service
app = Flask(__name__, static_folder='templates', static_url_path='')
app.debug = True


"""

API

"""

@app.route('/outlet/<num>/', methods=['GET'])
def get_out(num):
  pin = out[int(num)]
  return jsonify(id=int(num), value=pin.value)

@app.route('/outlet/<num>/', methods=['PUT'])
def set_out(num):
  pin = out[int(num)]
  requestJson = json.loads(request.data)
  pin.value = int(requestJson['value'])
  return jsonify(id=int(num), value=pin.value)

"""

@app.route('/pwm/')
def get_out2():
  return jsonify(name='out2', value=out2.value)

@app.route('/pwm/<val>')
def set_out2(val):
  out2.value = float(val)
  return jsonify(name='out2', value=out2.value)
"""




"""

Pages

"""
@app.route('/')
def index():
  return render_template('index.html', planet='Abydos')

# Entry point
if __name__ == '__main__':
  app.run(host='0.0.0.0')
