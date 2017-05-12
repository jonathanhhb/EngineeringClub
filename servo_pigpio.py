#!/usr/bin/python

import pigpio 
import time 
pi = pigpio.pi()

def feed():
	pi.set_servo_pulsewidth(18,600)
        time.sleep(0.5)
	pi.set_servo_pulsewidth(18,2200)
        time.sleep(0.5)
	pi.set_servo_pulsewidth(18,1500)

def turn_off():
	pi.set_servo_pulsewidth(18,600)

def turn_half():
	pi.set_servo_pulsewidth(18,1500)

def turn_full():
	pi.set_servo_pulsewidth(18,2200)
