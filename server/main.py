####################
# Hosts a websocket server on the port defined in constants.py
# Connect to it from the hosted apache2 server
####################

import RPi.GPIO as GPIO
from constants import *
from websocket_server import WebsocketServer
import time
import atexit

def print_at_lns_up(n, st, col=37):
	print("\033[" + str(n) + "F", end="", flush=True)
	print("\033[" + str(col) + ";1m" + (" "*40) + "\r" + st + "\033[0m", end="", flush=True)
	print("\033[" + str(n) + "E", end="", flush=True)

command_expands = {
	"fd": "Forwards",
	"bk": "Backwards",
	"hlt": "Stationary"
}

command_colours = {
	"fd":  35,
	"bk":  33,
	"hlt": 31
}

##########
#  GPIO  #
##########

def initgpio():
	GPIO.setmode(GPIO.BCM)

def initmotors():
	for p in MOT1: GPIO.setup(p, GPIO.OUT)
	for p in MOT2: GPIO.setup(p, GPIO.OUT)

def initleds():
	GPIO.setup(LED1, GPIO.OUT)

def setmotor(motor_number, enable, direction="clockwise"):
	if direction not in ["clockwise", "anticlockwise", "clock", "anti"]:
		print("Invalid direction")
		return
	if direction == "clock": direction = "clockwise"
	if direction == "anti": direction = "anticlockwise"
	if motor_number not in [1, 2]:
		print("Invalid motor number")
		return

	MOT = MOT1 if motor_number == 1 else MOT2

	GPIO.output(MOT[0], GPIO.HIGH if direction == "clockwise" else GPIO.LOW)
	GPIO.output(MOT[1], GPIO.LOW if direction == "clockwise" else GPIO.HIGH)
	GPIO.output(MOT[2], GPIO.HIGH if enable else GPIO.LOW)

def setled(state):
	GPIO.output(LED1, GPIO.HIGH if state else GPIO.LOW)


##########
# SERVER #
##########

def new_client(client, server):
	print_at_lns_up(1, "A client connected", 34)
	pass
def client_left(client, server):
	print_at_lns_up(1, "A client left!", 31)
	pass
def message_received(client, server, message):
	lines_up = 0
	display = ""
	colour = 37
	pieces = message.split("_")
	if pieces[0] == "motor1":
		lines_up = 3
		display = command_expands[pieces[1]]
		colour = command_colours[pieces[1]]
	elif pieces[0] == "motor2":
		lines_up = 5
		display = command_expands[pieces[1]]
		colour = command_colours[pieces[1]]
	else:
		if message ==  "led_test":
			lines_up = 1
			display = "Testing LED"
		if message == "motors_test":
			lines_up = 1
			display = "Testing motors"
	print_at_lns_up(lines_up, display, colour)
	if message == "led_test":
		for i in range(5):
			GPIO.output(LED1, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(LED1, GPIO.LOW)
			time.sleep(0.1)
	elif message == "motors_test":
		setmotor(1, True, "clock")
		setmotor(2, True, "clock")
		time.sleep(1)
		setmotor(2, False)
		time.sleep(1)
		setmotor(2, True, "clock")
		setmotor(1, False)
		time.sleep(1)
		setmotor(1, True, "anti")
		setmotor(2, True, "anti")
		time.sleep(1)
		setmotor(1, True, "clock")
		setmotor(2, True, "anti")
		time.sleep(4)
		setmotor(1, False)
		setmotor(2, False)
	elif message == "motor1_fd":
		setmotor(1, True, "clock")
	elif message == "motor1_bk":
		setmotor(1, True, "anti")
	elif message == "motor1_hlt":
		setmotor(1, False)
	elif message == "motor2_fd":
		setmotor(2, True, "clock")
	elif message == "motor2_bk":
		setmotor(2, True, "anti")
	elif message == "motor2_hlt":
		setmotor(2, False)

def onexit():
	GPIO.cleanup()
	print("Server exited")

atexit.register(onexit)

def serve():
	serv = WebsocketServer(PORT, HOST)
	serv.set_fn_new_client(new_client)
	serv.set_fn_client_left(client_left)
	serv.set_fn_message_received(message_received)

	print("\033[35m\033[1m== Latest instructions from web client ==\033[0m\n")
	print("= Left motor =\n\n= Right motor =\n\n= Other =\n")

	#print("\033[4AHello!", end="", flush=True)
	#print_at_lns_up(4, "Hello!")
	serv.run_forever()

if __name__ == "__main__":
	initgpio()
	print("[LOG] GPIO Initialised")
	initmotors()
	print("[LOG] Motors set up")
	initleds()
	print("[LOG] LEDs set up")
	print("[WEBSOCKET] Server running, waiting for connections...")
	serve()
