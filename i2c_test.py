#!/usr/bin/python

import smbus
import math
import os
from time import sleep
import time
import datetime

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
temp_H = 0x41
temp_L = 0x42

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
f = open('./i2c_test.txt','w')

try:
	while True:
		sleep(1)
                os.system('clear')

		print "gyro data"
		print "---------"
		print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') 
		t_H = read_word_2c(temp_H)
		TEMP = (t_H  /340) + 36.5

		gyro_xout = read_word_2c(0x43)
		gyro_yout = read_word_2c(0x45)
		gyro_zout = read_word_2c(0x47)

		print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
		print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
		print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)
		print "Raw Temp : ", t_H
		print "TEMP     : ", TEMP , " C"
		print "TEMP     : ", ((TEMP * 1.8) + 32), " F"
		f.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + " ")
		f.write( str(TEMP) + " " )
		f.write(" C\r\n")
		print
		print "accelerometer data"
		print "------------------"

		accel_xout = read_word_2c(0x3b)
		accel_yout = read_word_2c(0x3d)
		accel_zout = read_word_2c(0x3f)

		accel_xout_scaled = accel_xout / 16384.0
		accel_yout_scaled = accel_yout / 16384.0
		accel_zout_scaled = accel_zout / 16384.0

		print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
		print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
		print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

		print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

except KeyboardInterrupt:
		print " EXIT"
