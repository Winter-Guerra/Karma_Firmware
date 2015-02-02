#!/usr/bin/env python 

import time

# This file is the main Karma controller

# Let's test the servos
class Servo(object):
	calibration = {
	'wrist': {
		'min': 600000, 
		'max': 2100000,
		'gpioPin': 13,
		'pwmPin': 1
		},
	'hand': {
		'min': 400000, 
		'max': 2200000,
		'gpioPin': 12,
		'pwmPin': 0
		},

	'period': 20000000
	}
	
	def __init__(self, servoType):
		self.servoType = servoType
		self.enabled = False

		# Initialize the pins, but do not start PWM until the first PWM command has been given
		self.initializePins()


	# Setup functions
	def initializePins(self):
		# echo mode1 > /sys/kernel/debug/gpio_debug/gpio13/current_pinmux
		with open("/sys/kernel/debug/gpio_debug/gpio{}/current_pinmux".format(self.getGPIOPin()), "w") as pinmux:
			pinmux.write('mode1')
		
		# echo 1 > /sys/class/pwm/pwmchip0/export
		try:
			with open("/sys/class/pwm/pwmchip0/export", "w") as enablePWM:
				enablePWM.write(str(self.getPWMPin()))
		except:
			print "Pin {} is already setup as a PWM output. Skipping this setup step.".format(self.getPWMPin())

		# echo 20000000 > /sys/class/pwm/pwmchip0/pwm1/period
		with open("/sys/class/pwm/pwmchip0/pwm{}/period".format(self.getPWMPin()), "w") as period:
			period.write(str(self.getPeriod()))

		# Set the initial position location to be 90deg
		self.angle(90)

	# Main mapping PWM function
	def angle(self, angleValue):
		# Map the angle to a duty cycle value
		inputRange = (0.0, 180.0)
		outputRange = ( float(self.getMinDutyCycle()), float(self.getMaxDutyCycle()) )
		dutyCyleFloat = self.scale( angleValue, inputRange, outputRange)
		# Make the duty cycle an integer
		dutyCycle = int(round(dutyCyleFloat))
		# Set the duty cycle
		self.setDutyCycle(dutyCycle)

	# STATIC helper scaling function
	def scale(self, val, src, dst):
		#Scale the given value from the scale of src to the scale of dst.
		return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]



	# Commandline functions
	def setDutyCycle(self, dutyCycle):
		with open("/sys/class/pwm/pwmchip0/pwm{}/duty_cycle".format(self.getPWMPin()), "w") as duty_cycle:
			duty_cycle.write(str(dutyCycle))

	def enable(self):
		if not self.enabled:
			with open("/sys/class/pwm/pwmchip0/pwm{}/enable".format(self.getPWMPin()), "w") as enabledSwitch:
				enabledSwitch.write("1")
			self.enabled = True

	def disable(self):
		if self.enabled:
			with open("/sys/class/pwm/pwmchip0/pwm{}/enable".format(self.getPWMPin()), "w") as enabledSwitch:
				enabledSwitch.write("0")
			self.enabled = False

	# Getter functions
	def getMinDutyCycle(self):
		return Servo.calibration[self.servoType]['min']

	def getMaxDutyCycle(self):
		return Servo.calibration[self.servoType]['max']

	def getPeriod(self):
		return Servo.calibration['period']

	def getGPIOPin(self):
		return Servo.calibration[self.servoType]['gpioPin']

	def getPWMPin(self):
		return Servo.calibration[self.servoType]['pwmPin']

	
# This is just a test script
def testServo():
	wristServo = Servo('wrist')

	# Let's try to move the wrist back and forth
	wristServo.angle(0)
	wristServo.enable() ## THIS IS IMPORTANT!

	time.sleep(5)
	wristServo.angle(180)
	time.sleep(5)
	wristServo.angle(90)
	time.sleep(5)

	wristServo.disable()
	

	# Test the hand actuator
	handServo = Servo('hand')

	# Let's try to move the hand back and forth
	handServo.angle(0)
	handServo.enable() ## THIS IS IMPORTANT!

	time.sleep(5)
	handServo.angle(180)
	time.sleep(5)
	handServo.angle(90)
	time.sleep(5)

	handServo.disable()


# Check that everything works
if __name__ == '__main__':
	testServo()

