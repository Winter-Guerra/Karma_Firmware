#!/usr/bin/env python 

# Code is copyright Winter Guerra <winterg@mit.edu> February 2015, all rights reserved.

import time
from Servo import *
from myo import Myo
from myo_common import *

# This file is the main Karma controller

class Arm(object):


	# This will create the hand and wrist servos in the arm. This will also create the Myo instance.
	def __init__(self):

		# Create the actuators
		# self.wristServo = Servo('wrist')
		# self.handServo = Servo('hand')

		# Create the Myo controller sensor (with callbacks)
		self.myo = Myo(None) 

		# Start the Myo sensor.
		self.myo.connect()

		# Become slave to the myo sensor
		while True:
			self.myo.run()
		

	def openHand(self):
		pass
		# Open the hand, then disable the servo to save power/heat
		# self.handServo.angle(180)
		# self.handServo.enable()

		# Set a timer to turn off the servo in a minute


	def closeHand(self):
		pass
		# Close the hand, then disable the servo after a few minutes to save power/heat

		# self.handServo.angle(0)
		# self.handServo.enable()

		# Set a timer to turn off the servo in a minute


	def makeOpenCloseDecision(self):
		pass

	def makeWristRotationDecision(self):
		pass

def testArm():
	arm = Arm()

	# Do some stuff

if __name__ == '__main__':
	testArm()

