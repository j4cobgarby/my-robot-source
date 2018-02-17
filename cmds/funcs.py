import RPi.GPIO as GPIO
from constants import *
import time

def initmotors():
	GPIO.setmode(GPIO.BCM)
	for p in MOT1: GPIO.setup(p, GPIO.OUT)
	for p in MOT2: GPIO.setup(p, GPIO.OUT)

def setmotor(motor_number, enable, direction="clockwise"):
	if direction not in ["clockwise", "anticlockwise", "clock", "anti"]:
		print("Invalid direction")
		return
	if direction == "clock": direction = "clockwise"
	if direction == "anti": direction = "anticlockwise"
	if motor_number not in [1, 2]:
		print("Invalid motor number")
		return
	GPIO.setmode(GPIO.BCM)
	MOT = MOT1 if motor_number == 1 else MOT2

	GPIO.output(MOT[0], GPIO.HIGH if direction == "clockwise" else GPIO.LOW)
	GPIO.output(MOT[1], GPIO.LOW if direction == "clockwise" else GPIO.HIGH)
	GPIO.output(MOT[2], GPIO.HIGH if enable else GPIO.LOW)
