from __future__ import print_function

from collections import Counter, deque
import sys
import time
import math

from myo_common import *
from myo_raw import MyoRaw

class Myo(MyoRaw):
	'''Adds higher-level pose classification and handling onto MyoRaw.'''

	# This is calibrated to hold about 1min of data. This will be used to find the baseline muscle activity.
	HIST_LEN = 15 * 50 # 30 seconds at about 50hz
	MAX_SHORT_PULSE_TIME = 0.5 # seconds
	ARM_IDLE_CERTAINTY = 0.8 # certainty that arm is idle must be higher than this.
	MAX_MUSCLE_DIFFERENCE = 2.5 # Bicep and tricep cannot be more than 2x higher than each other.
	MIN_AMPLITUDE_THRESHOLD = 3 # All signals must be at least 4x larger than the norm.
	FRAMES_FOR_RECENT_ACTIVITY = int(0.25*50) #1/4 sec at 50hz

	# Callbacks is a dict
	def __init__(self, callbacks):
		# Initialize internals
		MyoRaw.__init__(self, None)
		self.callbacks = callbacks

		# FOR DEBUGGING
		self.callbacks = {
			'toggleHand': lambda: print("Toggling Hand (NOT IMPLIMENTED)")
		}

		# # Initiate the history. Initially, this list has an average of zero.
		self.history = deque([(1,1)], Myo.HIST_LEN)
		self.recentActivityList = deque([(1,1)], Myo.FRAMES_FOR_RECENT_ACTIVITY)


		# These vars are used later by logic
		self.lastRisingEdge = 0
		self.signalState = 'standby' # values can be 'standby', 'in_pulse', 'in_long_pulse'
		self.IMU_enable = False
		
		# Set the logic triggers
		# EMG
		self.add_emg_handler(self.edge_detector)

		self.add_emg_handler(lambda unused1, unused2: print( str( time.time() ) ) )

		# IMU
		

	def edge_detector(self, datapoint, moving):

		# Take our current datapoint and sort it for ease of use later.
		# Then, let's add it to our history
		sortedDatapoints = sorted(datapoint)
		self.history.append(sortedDatapoints)
		self.recentActivityList.append(sortedDatapoints)

		# Take an average of our history. This should be the baseline muscle activity.
		average_baseline = self.averageDatapoints(self.history)

		# Check if our last 0.25sec of recent activity has had relatively even muscle activity. I.E. bicep and tricep are within 2x of each other >90% of the time

		# Check for even muscle activity on the last 0.25 seconds
		percentageOfTimeMuscleIsValid = self.evenMuscleActivityTimePercentage(self.recentActivityList, Myo.MAX_MUSCLE_DIFFERENCE)
		
		if percentageOfTimeMuscleIsValid > Myo.ARM_IDLE_CERTAINTY:
			#print("percentage pass at {}".format(percentageOfTimeMuscleIsValid))
			
			# Now, check if the average muscle activity is higher than our average by at least 4x
			timesHighThanAverage = self.getHistoryTimesHigherThanAverage(self.recentActivityList, average_baseline)
			
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
		print("Detected rising edge")

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
			self.callbacks['toggleHand']()

		elif self.signalState is 'in_long_pulse':
			self.stopIMUCallbacks()

		# Set our new state
		self.signalState = 'standby'

	def startIMUCallbacks(self):
		print("starting IMU callbacks (NOT IMPLIMENTED)")

	def stopIMUCallbacks(self):
		print("stopping IMU callbacks (NOT IMPLIMENTED)")


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



