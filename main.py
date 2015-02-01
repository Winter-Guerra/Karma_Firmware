#!/usr/bin/env python 

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
		self.enable = False

		# Initialize the pins, but do not start PWM until the first PWM command has been given
		self.initializePins()


	# Setup functions
	def initializePins(self):
		# echo mode1 > /sys/kernel/debug/gpio_debug/gpio13/current_pinmux
		with open("/sys/kernel/debug/gpio_debug/gpio{}/current_pinmux".format(self.getGPIOPin()), "w") as pinmux:
			pinmux.write('mode1')
		# echo 1 > /sys/class/pwm/pwmchip0/export
		with open("/sys/class/pwm/pwmchip0/pwm{}/period".format(self.getPWMPin()), "w") as setPWMType:
			setPWMType.write("1")
		# echo 20000000 > /sys/class/pwm/pwmchip0/pwm1/period
		with open("/sys/class/pwm/pwmchip0/pwm{}/period".format(self.getPWMPin()), "w") as period:
			period.write(self.getPeriod())

	# Main mapping PWM function
	def angle(self, angleValue):
		# Map the angle to a duty cycle value
		dutyCyleFloat = self.scale(angleValue, (0.0, 100.0), (float(self.getMinDutyCycle())), float(self.getMaxDutyCycle()))
		print dutyCyleFloat
		# Make the duty cycle an integer
		dutyCycle = int(round(dutyCyleFloat))
		print dutyCycle
		# Set the duty cycle
		self.setDutyCycle(dutyCycle)

	# Helper scaling function
	def scale(val, src, dst):
		#Scale the given value from the scale of src to the scale of dst.
		return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]



	# Commandline functions
	def setDutyCycle(self, dutyCycle):
		with open("/sys/class/pwm/pwmchip0/pwm{}/duty_cycle".format(self.getPWMPin()), "w") as duty_cycle:
			duty_cycle.write(dutyCycle)

	def enable(self):
		if not self.enable:
			with open("/sys/class/pwm/pwmchip0/pwm{}/enable".format(self.getPWMPin()), "w") as enabledSwitch:
				enabledSwitch.write(1)
			self.enable = True

	def disable(self):
		if self.enable:
			with open("/sys/class/pwm/pwmchip0/pwm{}/enable".format(self.getPWMPin()), "w") as enabledSwitch:
				enabledSwitch.write(0)
			self.enable = False

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

	# Should know how to configure itself for the specific type of servo


# Check that everything works
if __name__ == '__main__':
	wristServo = Servo('wrist')

	# Check that the servo is properly calibrated
	# print 'Max ', wristServo.getMaxDutyCycle()
	# print 'Min ', wristServo.getMinDutyCycle()
	