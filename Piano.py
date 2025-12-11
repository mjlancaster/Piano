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
def playSong(path, t, moveSpeed):
    # Zero all solenoids first
    zeroSols()
    # Arbitrarily brief pause before beginning, may not be necessary
    sleep(0.25)
    with open(path, mode ='r')as file:
        song = csv.reader(file)
        for chord in song:
            # If "s" tag --> set current location
            if (chord[0].startswith("s")):
                location = int(chord[0][1:])
            # If "m" tag --> moveTo
            elif (chord[0].startswith("m")):
                destination = int(chord[0][1:])
                print("moving from {location} to: {destination}")
                moveTo(location, destination, 3, moveSpeed)
            # If an actual chord, play chord
            else:
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

# Returns INDEX of identified color in colors_RGB_norm[]
def guessColor():
    r,g,b,c = sensor.color_raw
    color = normalize([r, g, b])
    guess = 0
    mindist = 80000
    for i in range(len(colors_RGB_norm)):
        distance = math.dist(color, colors_RGB_norm[i])
        if mindist >= distance:
            guess = i
            mindist = distance
    print("guess: ", colors_name[guess], " r: ", r, " g ", g, " b: ", b)
    return guess

def moveTo(origin, target, thresh, speed):
    # Direction: 0 = left, 1 = right
    direction = int(target > origin)

    currentKey = origin

    # The color currently being observed (initialization)
    colorSeen = keys[origin]

    # Degenerate case
    if (origin == target):
        return
    
    # Counts number of consec. instances of new color
    i = 0

    # Start motor
    # If moving right:
    if (direction):
        motor_right.value = speed
        motor_left.value = 1.0
    # If moving left:
    else:
        motor_left.value = speed
        motor_right.value = 1.0

    # While motor is moving
    while (currentKey != target):
        # If moving right
        if (direction):
            prevColorSeen = colorSeen
            colorSeen = guessColor()
            if (colorSeen != keys[currentKey] and (i == 0 or colorSeen == prevColorSeen)):
                i += 1
                if (i == thresh):
                    # We have moved to a new color - which color?
                    # If moved 1 color (no skipping) in correct direction:
                    if (colorSeen - keys[currentKey] == 1 or colorSeen - keys[currentKey] == -2):
                        currentKey += 1
                    # If moved 2 color (skipped once) in correct direction:
                    elif (colorSeen - keys[currentKey] == 2 or colorSeen - keys[currentKey] == -1):
                        print("skipped key")
                        currentKey += 2
            else:
                i = 0
        # If moving left
        else:
            prevColorSeen = colorSeen
            colorSeen = guessColor()
            if (colorSeen != keys[currentKey] and (i == 0 or colorSeen == prevColorSeen)):
                i += 1
                if (i == thresh):
                    # We have moved to a new color - which color?
                    # If moved 1 color (no skipping) in correct direction:
                    if (colorSeen - keys[currentKey] == -1 or colorSeen - keys[currentKey] == 2):
                        currentKey -= 1
                    # If moved 2 color (skipped once) in correct direction:
                    elif (colorSeen - keys[currentKey] == -2 or colorSeen - keys[currentKey] == 1):
                        print("skipped key")
                        currentKey -= 2
            else:
                i = 0
    
    # We are now at the correct color --> shut off the motor
    motor_left.value = 1.0
    motor_right.value = 1.0

    # Update location
    location = target

    # OLD CODE :P
    """ while True:
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
        if (i == thresh):
            motor_right.value = 1.0
            motor_left.value = 1.0
            print("breaking")
            break """

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
colors_name = ["red", "blue", "green"]
colors_RGB = [[20, 5, 5], [4, 4, 4], [8, 10, 5]]
colors_RGB_norm = []
for item in colors_RGB:
    colors_RGB_norm.append(normalize(item))
keys = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0]
print("Color sensor initializations complete")

# Path of song file (.csv) - must be located in the project directory
song_path = "song.csv"

# Set tempo
bpm = 120
tick = 30.0 / float(bpm)

# Store current location
location = 0

# Initialize motors to 1.0 duty cycle (due to inversion)
motor_left.value = 1.0
motor_right.value = 1.0
sleep(1)
print("Motors initialized to 1.0")

# Test fire solenoids
#sol0.on()
#sleep(1.0)
#sol0.off()

playSong(song_path, tick, 0.8)

# Play the song
""" playSong(song_path, tick)
motor_right.value = 0.9
sleep(3)
motor_right.value = 1.0
sleep(0.5)
playSong(song_path, tick)
motor_left.value = 0.9
sleep(6)
motor_left.value = 1.0
sleep(0.5)
playSong(song_path, tick) """

sol0.off()
sol1.off()
sol2.off()
sol3.off()
sol4.off()

# MOTOR TESTS
# Drive left motor
#motor_left.value = 0.5
#sleep(1.0)
#motor_left.value = 1.0
#sleep(1.0)
#motor_right.value = 0.5
#sleep(1.0)
#motor_right.value = 1.0
