#!/usr/bin/env python 

# Code is copyright Winter Guerra <winterg@mit.edu> February 2015, all rights reserved.

import time
import threading
import sys

from Servo import *
from myo import Myo
from myo_common import *

# This file is the main Karma controller

class Arm(object):

	MOTOR_IDLE_TIME = 2 # seconds
	WRIST_SPEED = 25 # a scalar on the relative rotation speed for the updateWristRotation() callback


	# This will create the hand and wrist servos in the arm. This will also create the Myo instance.
	def __init__(self):

		# Create the actuators
		self.wristServo = Servo('wrist')
		self.handServo = Servo('hand')

		# Create state variables
		self.handStatus = 'opened' # args can be 'opened', 'closed'
		self.handResetTimer = None # Used to turn off the motor after 2 seconds of inactivity
		self.wristResetTimer = None

		# Center motors (not needed)
		# self.openHand()
		# self.setWristPosition(90) # deg

		# Create the Myo controller sensor (with callbacks)
		callbacks = {
			'toggleHand': self.toggleHand,
			'updateWristRotation': self.updateWristRotation,
			'isHandClosed': self.isHandClosed
		}

		self.myo = Myo(callbacks) 


		# Kill the script if the myo does not connect on time.
		killTimer = threading.Timer(5, self.killScript)
		killTimer.start()

		# Start the Myo sensor.
		self.myo.connect()

		# Kill the kill timer
		killTimer.cancel()

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

	def isHandClosed(self):
		if self.handStatus is 'closed':
			return True
		else:
			return False

	
	def setWristPosition(self, deg):
		# Each time that this is called
		self.wristServo.angle(deg)
		self.wristServo.enable()
		# turn off the servo after a few seconds
		self.setWristTimer()

	def updateWristRotation(self, offsetRadians):
		# Get the current angle of the servo
		currentAngle = self.wristServo.getAngle()

		# Figure out where the servo should go
		newAngle = currentAngle + offsetRadians * Arm.WRIST_SPEED

		self.wristServo.angle(newAngle)
		self.wristServo.enable()
		# turn off the servo after a few seconds
		self.setWristTimer()

	def killScript(self):
		sys.exit(1) # exit with error code

		


def testArm():
	arm = Arm()

	# Do some stuff

if __name__ == '__main__':
	testArm()

