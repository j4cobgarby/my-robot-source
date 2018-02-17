#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from constants import *
from funcs import *

initmotors()

print("motor on")
print("forwards")
setmotor(1, True, "clock")
setmotor(2, True, "clock")

sleep(3)

print("and now back")
setmotor(1, True, "anti")
setmotor(2, True, "anti")

sleep(3)

print("motor off")
setmotor(1, False)
setmotor(2, False)

GPIO.cleanup()
