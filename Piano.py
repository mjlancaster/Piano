from gpiozero import DigitalOutputDevice, PWMOutputDevice, Motor, LED
from time import sleep
import board
import adafruit_tcs34725
import math
import csv

# Helper function - plays the chord encoded in a row of the .csv
def playChord(chord):
    if (chord[0] == '1'):
        sol0.on()
    elif (chord[0] == '-' and sol0.value == 1):
        sol0.off()
    if (chord[1] == '1'):
        sol1.on()
    elif (chord[1] == '-' and sol1.value == 1):
        sol1.off()
    if (chord[2] == '1'):
        sol2.on()
    elif (chord[2] == '-' and sol2.value == 1):
        sol2.off()
    if (chord[3] == '1'):
        sol3.on()
    elif (chord[3] == '-' and sol3.value == 1):
        sol3.off()
    if (chord[4] == '1'):
        sol4.on()
    elif (chord[4] == '-' and sol4.value == 1):
        sol4.off()

# Helper function - zeroes all solenoids
def zeroSols():
    sol0.off()
    sol1.off()
    sol2.off()
    sol3.off()
    sol4.off()

# Plays the song encoded in the .csv found at path, at tick speed t
def playSong(path, t):
    # Zero all solenoids first
    zeroSols()
    # Arbitrarily brief pause before beginning, may not be necessary
    sleep(0.5)
    with open(path, mode ='r')as file:
        song = csv.reader(file)
        for chord in song:
            playChord(chord)
            sleep(t)
            
def normalize(colors):
    length = 0
    for item in colors:
        length = length + item**2
        
    length = math.sqrt(length)
    colors_norm = []
        
    for item in colors:
        colors_norm.append(item/max(length,1))
        
    return colors_norm

def guessColor(r, g, b, ref_colors):
    color = normalize([r, g, b])
    guess = 0
    mindist = 80000
    for i in range(len(ref_colors)):
        distance = math.dist(color, ref_colors[i])
        if mindist >= distance:
            guess = i
            mindist = distance
    
    return guess

def getLocation():
    r,g,b,c = sensor.color_raw
    guess = guessColor(r, g, b, colors_RGB_norm)
    print("guess: ", colors_name[guess], " r: ", r, " g ", g, " b: ", b)
    return guess

def moveTo(target, thresh):
    i = 0
    while True:
        location = getLocation()
        if (location < target):
            i = 0
            if (motor_left.value != 1.0):
                motor_left.value = 1.0
                sleep(0.25)
            else:
                motor_left.value = 1.0
            motor_right.value = 0.8
        elif (location > target):
            i = 0
            if (motor_right.value != 1.0):
                motor_right.value = 1.0
                sleep(0.25)
            else:
                motor_right.value = 1.0
            motor_left.value = 0.8
        else:
            i += 1
        if (i == 3):
            motor_right.value = 1.0
            motor_left.value = 1.0
            print("breaking")
            break

# Assign solenoid pins
sol0 = DigitalOutputDevice(22)
sol1 = DigitalOutputDevice(27)
sol2 = DigitalOutputDevice(17)
sol3 = DigitalOutputDevice(24)
sol4 = DigitalOutputDevice(25)

# Set PWM frequency
pwm_freq = 5000

# Assign motor pins
motor_left = PWMOutputDevice(5)
motor_left.frequency = pwm_freq
motor_right = PWMOutputDevice(6)
motor_right.frequency = pwm_freq

# Initializations for color sensor
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)
colors_name = ["red", "green", "pink", "yellow", "blue"]
colors_RGB = [[20, 5, 5], [8, 10, 5], [12, 5, 5], [33, 23, 9], [4, 4, 4]]
colors_RGB_norm = []
for item in colors_RGB:
    colors_RGB_norm.append(normalize(item))
print("Color sensor initializations complete")

# Path of song file (.csv) - must be located in the project directory
song_path = "song.csv"

# Set tempo
bpm = 260
tick = 60.0 / float(bpm)

# Initialize motors to 1.0 duty cycle (due to inversion)
motor_left.value = 1.0
motor_right.value = 1.0
print("sleeping now")
sleep(10)
print("sleeping again")
sleep(5)
print("Motors initialized to 1.0")

# Test fire solenoids
#sol0.on()
#sleep(1.0)
#sol0.off()

# Play the song
playSong(song_path, tick)

# MOTOR TESTS
# Drive left motor
#motor_left.value = 0.5
#sleep(1.0)
#motor_left.value = 1.0
#sleep(1.0)
#motor_right.value = 0.5
#sleep(1.0)
#motor_right.value = 1.0

# Updates current location (index in colors_RGB_norm)
# location = getLocation()

# Set target (index in colors_RGB_norm)
# target = 1

# Number of consec. triggers necessary to stop
# threshold = 3

#Color motor tests
# print("Beginning motor tests")
# moveTo(target, threshold)
