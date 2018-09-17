from bottle import route, run
from flask import Flask, request,jsonify, make_response,Response

import logging
import RPi.GPIO as GPIO

pinButton_1 = 14
pinButton_2 = 15
pinButton_3 = 18

pinLed = 18
GPIO.setmode(GPIO.BCM)
# pin 17 as input with pull-up resistor
GPIO.setup(pinButton_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinButton_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinButton_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# pin 18 as output
GPIO.setup(pinLed, GPIO.OUT)

app = Flask(__name__)
# app = Flask(__name__, static_url_path='/tmp')

LedState = False

def read_button(pin):
	if GPIO.input(pin):
		# return 'Released'
		return 0
	else:
		# return 'Pressed'
		return 1

def update_led():
	GPIO.output(pinLed, LedState)
				
def toggleLed():
	global LedState
	LedState = not LedState



from flask import Flask, request
app = Flask(__name__, static_url_path='')

@app.route('/index/')
def root():
	return app.send_static_file('test.html')


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('test.html')
    return Response(content, mimetype="text/html")

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


# @app.route('/aa')
# def hello_world():
# 	res = "<!DOCTYPE html><html><title>HTML Tutorial</title><body><h1>This is a heading</h1><p>This is a paragraph.</p></body></html>"+ str(read_button())
# 	return res

# @route('/')
# @route('/<arg>')
# def index(arg=""):
# 	if arg == "toggle":
# 		toggleLed()
					
# 	update_led()
	
# 	response = "<html>\n"
# 	response += "<body>\n"
# 	response += "<script>\n"
# 	response += "function changed()\n"
# 	response += "{window.location.href='/toggle'}\n"
# 	response += "</script>\n"
	
# 	response += "Button: " + read_button() +"\n"
# 	response += "<br/><br/>\n"
# 	response += "<input type='button' onClick='changed()' value=' LED '/>\n"
# 	response += "</body></html>\n"
# 	return response

# @route('/view')
# def view(arg=""):	
# 	response = "aaa";
# 	return response



@app.errorhandler(404)
def not_found(error):
	# app.logger.info('this is a string')
	# app.logger.debug('A value for debugging')
	# app.logger.warning('A warning occurred (%d apples)', 42)
	app.logger.error('An error occurred')
	return make_response(jsonify({'error': 'Not found'}), 404)

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        print ("record",record.url,request.remote_addr,type(record),type(request.remote_addr))
        return super().format(record)

if __name__ == '__main__':
	# get_day = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
	handler = logging.FileHandler('flask.log', encoding='UTF-8')
	handler.setLevel(logging.DEBUG)
	logging_format = logging.Formatter(
		'%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
	# logging_format = RequestFormatter(
	# 	'[%(asctime)s] %(remote_addr)s requested %(url)s\n'
	# 	'%(levelname)s in %(module)s: %(message)s'
	# )
	handler.setFormatter(logging_format)
	app.logger.addHandler(handler)
	# https://segmentfault.com/q/1010000002595388
	app.run(host='0.0.0.0',debug=True,port=80)
	client.close()
