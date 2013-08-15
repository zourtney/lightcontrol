#import copy
#from time import sleep
import json
from flask import Flask, jsonify, render_template, request
from gpiocrust import Header, OutputPin#, PWMOutputPin, InputPin

# Set up Raspberry Pi I/O
header = Header()
out1 = OutputPin(11)
#out2 = PWMOutputPin(13)
#in1 = InputPin(15)


# Super simple web service
app = Flask(__name__, static_folder='templates', static_url_path='')
app.debug = True


"""

API

"""

@app.route('/out/', methods=['GET'])
def get_out1():
  return jsonify(name='out1', value=out1.value)

@app.route('/out/', methods=['PUT'])
def set_out1():
  requestJson = json.loads(request.data)
  out1.value = int(requestJson['value'])
  return jsonify(name='out1', value=out1.value)
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