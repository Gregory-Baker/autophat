# Initio Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python motorTest2.py

from __future__ import print_function
import time
#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

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

		self.myMotor.set_drive(0,0,150)
		self.myMotor.set_drive(1,1,150)


	def forward(self, speed):

		if self.myMotor.connected == False:
			print("Motor Driver not connected. Check connections.", \
				file=sys.stderr)
			return

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

def readchar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	if ch == '0x03':
		raise KeyboardInterrupt
	return ch

def readkey(getchar_fn=None):
	getchar = getchar_fn or readchar
	c1 = getchar()
	if ord(c1) != 0x1b:
		return c1
	c2 = getchar()
	if ord(c2) != 0x5b:
		return c1
	c3 = getchar()
	return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

speed = 100

print("Tests the motors by using the arrow keys to control")
print("Use , or < to slow down")
print("Use . or > to speed up")
print("Speed changes take effect when the next arrow key is pressed")
print("Press Ctrl-C to end")
print()

autophat = Autophat()
myMotor = qwiic_scmd.QwiicScmd()
if myMotor.connected == True:
	print("connected")
myMotor.begin()
time.sleep(.250)

# main loop
try:
	while True:
		keyp = readkey()
		if keyp == 'w' or ord(keyp) == 16:
			print('Forward', speed)
			while True:
				myMotor.set_drive(0,0,200)
				myMotor.set_drive(1,1,200)
				time.sleep(.05)
		elif keyp == 's' or ord(keyp) == 17:
			autophat.reverse(speed)
			print('Reverse', speed)
		elif keyp == 'd' or ord(keyp) == 18:
			autophat.spinRight(speed)
			print('Spin Right', speed)
		elif keyp == 'a' or ord(keyp) == 19:
			autophat.spinLeft(speed)
			print('Spin Left', speed)
		elif keyp == '.' or keyp == '>':
			speed = min(200, speed+10)
			if (abs(speed) < 100):
				speed = 100
			print('Speed+', speed)
		elif keyp == ',' or keyp == '<':
			speed = max (0, speed-10)
			if (abs(speed) < 100):
				speed = 0
			print('Speed-', speed)
		elif keyp == ' ':
			autophat.stop()
			print('Stop')
		elif ord(keyp) == 3:
			break

except KeyboardInterrupt:
	print

finally:
	autophat.cleanup()
