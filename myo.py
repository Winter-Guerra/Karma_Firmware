from __future__ import print_function

from collections import Counter, deque
import sys
import time
import math
import random

from myo_common import *
from myo_raw import MyoRaw
# NO U
#from Quaternion import *

class Myo(MyoRaw):
	'''Adds higher-level pose classification and handling onto MyoRaw.'''

	# This is calibrated to hold about 1min of data. This will be used to find the baseline muscle activity.
	AVERAGE_SAMPLE_RATE = 5 # HZ for the rolling average
	AVERAGE_SAMPLE_MODULO = 50/AVERAGE_SAMPLE_RATE
	HIST_LEN = int( (10*AVERAGE_SAMPLE_RATE)) # 10 seconds at about 10hz (downsampled), 
	MAX_SHORT_PULSE_TIME = 0.5 # seconds
	ARM_IDLE_CERTAINTY = 0.7 # certainty that arm is idle must be higher than this.
	MAX_MUSCLE_DIFFERENCE = 3 # Bicep and tricep cannot be more than 2x higher than each other.
	MIN_AMPLITUDE_THRESHOLD = 2 # All signals must be at least 3x larger than the norm.
	FRAMES_FOR_RECENT_ACTIVITY = int(0.25*50) #1/4 sec at 50hz

	# Callbacks is a dict
	def __init__(self, callbacks):
		# Initialize internals
		MyoRaw.__init__(self, None)
		self.callbacks = callbacks

		# FOR DEBUGGING
		# self.callbacks = {
		# 	'toggleHand': lambda: print("Toggling Hand (NOT IMPLIMENTED)"),
		# 	'updateWristRotation': lambda: print("Rotating wrist (NOT IMPLIMENTED)")
		# }

		# # Initiate the history. Initially, this list has an average of zero.
		self.rollingHistory = deque([(1,1)], Myo.HIST_LEN)
		self.rollingHistoryModuloCounter = 0
		self.recentActivityList = deque([(1,1)], Myo.FRAMES_FOR_RECENT_ACTIVITY)


		# These vars are used later by logic
		self.lastRisingEdge = 0
		self.signalState = 'standby' # values can be 'standby', 'in_pulse', 'in_long_pulse'
		self.IMU_Enabled = False # 
		self.startingQuaternion = None # Keep this at None when not in use
		self.startingRoll = None

		
		# Set the logic triggers
		# EMG
		self.add_emg_handler(self.edge_detector)

		# For debugging
		#self.add_emg_handler(lambda unused1, unused2: print( str( time.time() ) ) )

		# IMU
		# def debugIMU(quat, accel, gyro):
		# 	if random.randrange(1,10) is 1:
		# 			print(quat, accel, gyro)

		# 	#print(quat, accel, gyro)
		self.add_imu_handler(self.IMUCallback)
		

	def edge_detector(self, datapoint, moving):

		# Take our current datapoint and sort it for ease of use later.
		# Then, let's add it to our history
		sortedDatapoints = sorted(datapoint)
		self.recentActivityList.append(sortedDatapoints)

		# Let's take a rolling muscle average, downsampled to a reasonable rate
		if self.rollingHistoryModuloCounter >= Myo.AVERAGE_SAMPLE_MODULO:
			self.rollingHistoryModuloCounter = 0

			# If our signal is not currently "HIGH", we should update our rolling muscle average.
			if self.signalState is 'standby':
				self.rollingHistory.append(sortedDatapoints)
		else:
			self.rollingHistoryModuloCounter += 1

		# Take an average of our history. This should be the baseline muscle activity.
		self.average_baseline = self.averageDatapoints(self.rollingHistory)

		# Check if our last 0.25sec of recent activity has had relatively even muscle activity. I.E. bicep and tricep are within 2x of each other >90% of the time

		# Check for even muscle activity on the last 0.25 seconds
		percentageOfTimeMuscleIsValid = self.evenMuscleActivityTimePercentage(self.recentActivityList, Myo.MAX_MUSCLE_DIFFERENCE)
		
		if percentageOfTimeMuscleIsValid > Myo.ARM_IDLE_CERTAINTY:
			#print("percentage pass at {}".format(percentageOfTimeMuscleIsValid))
			
			# Now, check if the average muscle activity is higher than our average by at least 4x
			timesHighThanAverage = self.getHistoryTimesHigherThanAverage(self.recentActivityList, self.average_baseline)
			
			if timesHighThanAverage > Myo.MIN_AMPLITUDE_THRESHOLD:
				# Then, we have a rising edge.
				self.detectedRisingEdge()
				return
		else:
			#print("Arm moving. Not making a signal.")
			pass

		# If we make it here, we detected a falling edge
		self.detectedFallingEdge()


		# Check if we have had 0.25 secs of recent activity that are above this threshold. If so, we probably have the rising edge of a signal.

	def averageDatapoints(self, datapoints):
		# Take an average of our history. This should be the baseline muscle activity.
		total = 0
		for datapoint in datapoints:
			total = total + sum(datapoint) # 
		
		average = total/len(datapoints)
		return average

	def evenMuscleActivityTimePercentage(self, datapoints, upperLimit):
		# Go through each sorted datapoint and get the high and low muscle readings
		passingDatapoints = []
		for datapoint in datapoints:
			highMuscleSensors = datapoint[-4:]
			highMuscleSensorValue = sum(highMuscleSensors)

			lowMuscleSensors = datapoint[:4]
			lowMuscleSensorValue = sum(lowMuscleSensors)

			# Check if the muscle values are kind of equal
			datapointPasses = (float(highMuscleSensorValue)/lowMuscleSensorValue < upperLimit )
			
			# Log if this datapoint was valid
			passingDatapoints.append( 1 if datapointPasses else 0 )

		# Check the percentage of the time that all muscles had valid data
		return float(sum(passingDatapoints))/len(passingDatapoints)

	def getHistoryTimesHigherThanAverage(self, datapoints, average_baseline):
		# Check how many times higher is the recent activity to the avg baseline
		recentAverageActivity = self.averageDatapoints(datapoints) 

		return recentAverageActivity/float(average_baseline) 

	def detectedRisingEdge(self):
		# Hint, states that we can be in are 'standby', 'in_pulse', 'in_long_pulse'

		# DEBUG
		#print("Detected rising edge", time.time())

		if self.signalState is 'standby':
			
			self.signalState = 'in_pulse'
			# Log the time that we started seeing this signal
			self.lastRisingEdge = time.time()
			# Do nothing more, we must wait for the falling edge to trigger the short pulse command

		elif self.signalState is 'in_pulse':
			# Check if this signal has become a long_pulse
			currentTime = time.time()

			if currentTime - self.lastRisingEdge > Myo.MAX_SHORT_PULSE_TIME:
				# Then, this signal has become a long pulse
				self.signalState = 'in_long_pulse'
				# trigger the long pulse callback
				self.startIMUCallbacks()

		elif self.signalState is 'in_long_pulse':
			# We don't really have to do anything here until the signal goes down again. The IMU callbacks will be going strong during this time
			pass


	def detectedFallingEdge(self):

		# DEBUG
		#print("Detected falling edge")

		if self.signalState is 'standby':
			# do nothing
			pass

		elif self.signalState is 'in_pulse':
			# Then we should tell the hand to open and close
			print("Toggling hand.")
			self.callbacks['toggleHand']()

		elif self.signalState is 'in_long_pulse':
			self.stopIMUCallbacks()

		# Set our new state
		self.signalState = 'standby'

	def startIMUCallbacks(self):
		print("starting IMU callbacks")

		# Start the callback
		self.IMU_Enabled = True

	def stopIMUCallbacks(self):
		print("stopping IMU callbacks")

		self.IMU_Enabled = False 

	def IMUCallback(self, quat, accel, gyro):
		# Check if we can continue with our callback
		if self.IMU_Enabled:

			# Check if we need to take a reference quaternion
			#if not self.startingQuaternion:
			if not self.startingRoll:
				# For Quaternions
				# normalizedQuaternionArray = normalize(quat)
				# self.startingQuaternion = Quat(normalizedQuaternionArray)
				
				# Without Numpy
				x = quat[0]
				y = quat[1]
				z = quat[2]
				w = quat[3]

				self.startingRoll  = -math.atan2(2*y*z + 2*w*x, -w*w + x*x + y*y - z*z)


			else:
				# WITH NUMPY
				# we should do some math to see how much we have rolled.
				# currentQuaternionArray = normalize(quat)
				# currentQuaternion = Quat(currentQuaternionArray)

				# # Take the current position and multiply that with the inverse of the original position (to get a local delta)
				# differenceQuat = currentQuaternion / self.startingQuaternion

				# # Take the roll component out of the quat
				# print(differenceQuat.roll)

				# WITHOUT NUMPY
				x = quat[0]
				y = quat[1]
				z = quat[2]
				w = quat[3]

				currentRoll  = -math.atan2(2*y*z + 2*w*x, -w*w + x*x + y*y - z*z)

				# Subtract the starting roll from the current roll
				differenceRoll = currentRoll - self.startingRoll
				# Debug
				#print("Angle:", differenceRoll)
				self.callbacks['updateWristRotation'](differenceRoll)
				

		else:
			# Reset our saved position
			self.startingQuaternion = None
			self.startingRoll = None

	# MATH functions

	def average(self, datapoint): 
		# Take an average of the datapoint
		return sum(datapoint) * 1.0 / len(datapoint)

	def variance(self, datapoint):
		# Take a variance of this datapoint
		map(lambda x: (x - avg)**2, datapoint)

	def std(self, datapoint):
		# Take the variance of the datapoint
		var = self.variance(datapoint)
		# Take the STD of the datapoint using the variance
		stdeviation = math.sqrt(self.average(var))



