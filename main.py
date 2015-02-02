#!/usr/bin/env python 

# Code is copyright Winter Guerra <winterg@mit.edu> February 2015, all rights reserved.

import time
import threading

from Servo import *
from myo import Myo
from myo_common import *

# This file is the main Karma controller

class Arm(object):

	MOTOR_IDLE_TIME = 2 # seconds


	# This will create the hand and wrist servos in the arm. This will also create the Myo instance.
	def __init__(self):

		# Create the actuators
		self.wristServo = Servo('wrist')
		self.handServo = Servo('hand')

		# Create state variables
		self.handStatus = 'opened' # args can be 'opened', 'closed'
		self.handResetTimer = None # Used to turn off the motor after 2 seconds of inactivity
		self.wristResetTimer = None

		# Center motors
		self.openHand()
		self.updateWristRotation(90) # deg

		# Create the Myo controller sensor (with callbacks)
		callbacks = {
			'toggleHand': self.toggleHand,
			'updateWristRotation': self.updateWristRotation
		}

		self.myo = Myo(callbacks) 

		# Start the Myo sensor.
		self.myo.connect()

		# Become slave to the myo sensor
		while True:
			self.myo.run()

	
	def setHandTimer(self):
		# Stop the old timer if it exists
		if self.handResetTimer:
			self.handResetTimer.cancel()

		self.handResetTimer = threading.Timer(Arm.MOTOR_IDLE_TIME, self.handServo.disable)
		self.handResetTimer.start()

	def setWristTimer(self):
		if self.wristResetTimer:
			self.wristResetTimer.cancel()

		self.wristResetTimer = threading.Timer(Arm.MOTOR_IDLE_TIME, self.wristServo.disable)
		self.wristResetTimer.start()
		

	def openHand(self):
		# Open the hand, then disable the servo to save power/heat
		self.handServo.angle(180)
		self.handServo.enable()

		# Set a timer to turn off the servo soon
		self.setHandTimer()

	def closeHand(self):
		# Close the hand, then disable the servo after a few minutes to save power/heat

		self.handServo.angle(0)
		self.handServo.enable()

		# Set a timer to turn off the servo soon
		self.setHandTimer()

	def toggleHand(self):
		
		if self.handStatus is 'opened':
			self.closeHand()
			self.handStatus = 'closed'
		else:
			self.openHand()
			self.handStatus = 'opened'
		

	def updateWristRotation(self, deg):
		self.wristServo.angle(deg)
		self.wristServo.enable()
		# turn off the servo after a few seconds
		self.setWristTimer()

		


def testArm():
	arm = Arm()

	# Do some stuff

if __name__ == '__main__':
	testArm()

