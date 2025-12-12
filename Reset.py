from gpiozero import DigitalOutputDevice, PWMOutputDevice, Motor, LED
from time import sleep
import board
import adafruit_tcs34725
import math
import csv

pwm_freq = 5000

motor_left = PWMOutputDevice(5)
motor_left.frequency = pwm_freq
motor_right = PWMOutputDevice(6)
motor_right.frequency = pwm_freq

motor_left.value = 1.0
motor_right.value = 1.0

sol0 = DigitalOutputDevice(22)
sol1 = DigitalOutputDevice(27)
sol2 = DigitalOutputDevice(17)
sol3 = DigitalOutputDevice(24)
sol4 = DigitalOutputDevice(25)

sol0.off()
sol1.off()
sol2.off()
sol3.off()
sol4.off()

print('reset')