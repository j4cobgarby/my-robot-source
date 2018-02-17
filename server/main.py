####################
# Hosts a websocket server on the port defined in constants.py
# Connect to it from the hosted apache2 server
####################

import RPi.GPIO as GPIO
from constants import *
from websocket_server import WebsocketServer
import time
import atexit

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
	print("New client connected!")

def client_left(client, server):
	print("Client left! :(")

def message_received(client, server, message):
	print("Client told us something!\n\tmessage: " + message)

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
