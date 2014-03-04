from webiopi.devices.analog import MCP3008
import threading
import RPi.GPIO as GPIO
import time
from bottle import route, run, debug, template, request, static_file, error

def interpret(str):
		if str == "spin":
				return SPIN
		if str == "counter":
				return CNTR
		if str == "calibrate":
				return CALB
		if str == "track":
				return TRAK
		if str == "stop":
				return STOP
		return UNKN

class WebThread(threading.Thread):
	def __init__(self ):
		threading.Thread.__init__(self)

	def run(self):
		run(host='0.0.0.0', port=8080)

	@route('/command')
	def login_form():
		return '''<form method="POST" action="/command">
			<input name="command"	 type="text" />
			<input type="submit" />
			  </form>'''

	@route('/command', method='POST')
	def login_submit():
		global status
		status = interpret(request.forms.get('command'))
		print (status) 
		return '''<form method="POST" action="/command">
			<input name="command"	 type="text" />
			<input type="submit" />
			  </form>
			<p>Message was entered</p>'''

def setStep(w1, w2, w3, w4):
	GPIO.output(coil_A_1_pin, w1)
	GPIO.output(coil_A_2_pin, w2)
	GPIO.output(coil_B_1_pin, w3)
	GPIO.output(coil_B_2_pin, w4)

def cntrspin():
        print ( "Counter Spinning" )
        moveCntrwise(10000)

def spin():
	print ( "Spinning" )
	moveClckwise(10000)

def calibrate():
	print ( "calibrating" )
	global position
	position = 0
	moveCntrwise ( NUM_READINGS_IN_CYCLE / 3 )
	print ( "Negative Calibrate Position :" + str(position) )
	i = NUM_READINGS_IN_CYCLE * 2 / 3
	reading = []
	while status != STOP and i > 0 :
		reading.append(readAnalog(2))
		moveClckwise(1)
		i -= 1
	print ( "Positive Calibrate Position :" + str(position) )
	goToPosition( reading.index(max(reading)) - ( NUM_READINGS_IN_CYCLE / 3 ) )

def track():
	print ( "Tracking" )
	while status != STOP :
		rght = readAnalog(0) + readAnalog(1)
		left = readAnalog(3) + readAnalog(4)
		r = left - rght
		print ( str(r))
		if r < -15:
			moveClckwise(3)
		elif r > 15:
			moveCntrwise(3)

def moveClckwise( steps ):
	print ( "Clockwise!" )
	global position
	steps = int ( steps )
	while  steps > 0 and status != STOP and position < ( NUM_READINGS_IN_CYCLE / 3 ):
		setStep(1, 0, 0, 1)
		time.sleep(delay)
		setStep(0, 1, 0, 1)
		time.sleep(delay)
		setStep(0, 1, 1, 0)
		time.sleep(delay)
		setStep(1, 0, 1, 0)
		time.sleep(delay)
		steps -= 1
		position += 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readAnalog(index):
	if ((index > 5) or (index < 0)):
		return -1
	return adc.analogRead(index)

def moveCntrwise( steps ):
	print ( "Cntrwise" )
	global position
	steps = int ( steps )
	while  steps > 0 and status != STOP and position > - ( NUM_READINGS_IN_CYCLE / 3):	
		setStep(1, 0, 1, 0)
		time.sleep(delay)
		setStep(0, 1, 1, 0)
		time.sleep(delay)
		setStep(0, 1, 0, 1)
		time.sleep(delay)
		setStep(1, 0, 0, 1)
		time.sleep(delay)
		steps -= 1
		position -= 1

def goToPosition( pos ):
	global position
	pos = int ( pos )
	print ("Going to Position: " + str(pos) + " From Position: " + str(position))
	if position > pos:
		moveCntrwise(position - pos)
	else:
		moveClckwise(pos - position)

SPIN = 0
CNTR = 5
CALB = 1
TRAK = 2
STOP = 3
UNKN = 4

NUM_READINGS_IN_CYCLE = 128

global position
position = 0
global status 
status = UNKN
wThread = WebThread()
wThread.daemon = 1
wThread.start()

coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 27
coil_B_2_pin = 22
delay = 5 / 1000.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

adc = MCP3008(chip=0)

while 1:
	if status == SPIN:
		print("gunna spin")
		spin()
	elif status == CNTR:
		print("gunna spin the other way")
		cntrspin()
	elif status == CALB:
		print("gunna calibrate")
		calibrate()
		status = STOP
	elif status == TRAK:
		print("gunna track")
		track()
