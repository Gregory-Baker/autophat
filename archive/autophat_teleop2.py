#!/usr/bin/env python
#-----------------------------------------------------------------------------
# A simple test to speed up and slow down both motors in opposite directions.
#------------------------------------------------------------------------
#
# Written by Mark Lindemer
# SparkFun Electronics, April 2020
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#

from __future__ import print_function
import time
import sys
import math
import qwiic_scmd

class Autophat:

	def __init__(self):
		self.myMotor = qwiic_scmd.QwiicScmd()

		self.R_MTR = 0
		self.L_MTR = 1
		self.FWD = 0
		self.BWD = 1

		if self.myMotor.connected == False:
			print("Motor Driver not connected. Check connections.", \
				file=sys.stderr)
			return
		self.myMotor.begin()
		print("Motor initialized.")
		time.sleep(.250)

		#self.myMotor.inversion_mode(1,1)

		# Zero speeds
		self.myMotor.set_drive(0,0,0)
		self.myMotor.set_drive(1,1,0)

		self.myMotor.enable()
		print("Motor enabled")
		time.sleep(.250)

	def forward(self, speed):
		self.myMotor.set_drive(self.R_MTR, self.FWD, speed)
		self.myMotor.set_drive(self.L_MTR, self.FWD, speed)

	def reverse(self, speed):
		self.myMotor.set_drive(self.R_MTR, self.BWD, speed)
		self.myMotor.set_drive(self.L_MTR, self.BWD, speed)

	def spinRight(self, speed):
		self.myMotor.set_drive(self.R_MTR, self.FWD, speed)
		self.myMotor.set_drive(self.L_MTR, self.BWD, speed)

	def spinLeft(self, speed):
		self.myMotor.set_drive(self.R_MTR, self.BWD, speed)
		self.myMotor.set_drive(self.L_MTR, self.FWD, speed)

	def stop(self):
		self.myMotor.set_drive(self.R_MTR, self.FWD, 0)
		self.myMotor.set_drive(self.L_MTR, self.FWD, 0)

	def cleanup(self):
		self.myMotor.disable()


def runExample():

	R_MTR = 0
	L_MTR = 1
	FWD = 0
	BWD = 1

	speed = 100

	while True:
		for speed in range(100,255):
			print(speed)
			autophat.myMotor.set_drive(R_MTR,FWD,speed)
			autophat.myMotor.set_drive(L_MTR,BWD,speed)
			time.sleep(.05)
		for speed in range(255,100,-1):
			print(speed)
			autophat.myMotor.set_drive(R_MTR,FWD,speed)
			autophat.myMotor.set_drive(L_MTR,BWD,speed)
			time.sleep(.05)

if __name__ == '__main__':
	autophat = Autophat()
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("Ending example.")
		autophat.myMotor.disable()
		sys.exit(0)

