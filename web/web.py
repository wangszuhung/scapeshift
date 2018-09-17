from flask import Flask  
from flask import render_template
from flask import Flask, request,jsonify, make_response,Response
import RPi.GPIO as GPIO

pinButton_1 = 14
pinButton_2 = 15
pinButton_3 = 18

pinLed = 19
GPIO.setmode(GPIO.BCM)
# pin 17 as input with pull-up resistor
# GPIO.setup(pinButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinButton_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinButton_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinButton_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# pin 18 as output
GPIO.setup(pinLed, GPIO.OUT)

# creates a Flask application, named app
app = Flask(__name__)
# app = Flask(__name__, static_url_path='/static')

def read_button(pin):
	if GPIO.input(pin):
		# return 'Released'
		return 0
	else:
		# return 'Pressed'
		return 1

@app.route('/api', methods=['GET'])
def api():
	# sudo journalctl -n
	# http://192.168.0.28/log?service=sudo%20journalctl%20-n
	re_service={
		"read_button_1":read_button(14),
		"read_button_2":read_button(15),
		"read_button_3":read_button(18),
		# "cpu_temp":read_cpu_temp(),
		# "datetime":str(checktime())
	}
	return jsonify(re_service)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)



# a route where we will display a welcome message via an HTML template
@app.route("/")
def aa():  
	message = "Hello, World"
	return message
	# return render_template('/templates/test.html', message=message)

# run the application
if __name__ == "__main__":  
	app.run(host='0.0.0.0',debug=True,port=80)
	client.close()
