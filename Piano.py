from gpiozero import DigitalOutputDevice, PWMOutputDevice, Motor
from time import sleep
import csv

# Helper function - plays the chord encoded in a row of the .csv
def playChord(chord):
    if (chord[0] == '1'):
        sol0.on()
    elif (chord[0] == '-' & sol0.value == 1):
        sol0.off()
    if (chord[1] == '1'):
        sol1.on()
    elif (chord[1] == '-' & sol1.value == 1):
        sol1.off()
    if (chord[2] == '1'):
        sol2.on()
    elif (chord[2] == '-' & sol2.value == 1):
        sol2.off()
    if (chord[3] == '1'):
        sol3.on()
    elif (chord[3] == '-' & sol3.value == 1):
        sol3.off()
    if (chord[4] == '1'):
        sol4.on()
    elif (chord[4] == '-' & sol4.value == 1):
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

# Assign solenoid pins
sol0 = DigitalOutputDevice(17)
sol1 = DigitalOutputDevice(27)
sol2 = DigitalOutputDevice(22)
sol3 = DigitalOutputDevice(5)
sol4 = DigitalOutputDevice(6)

# Assign motor pins
motor_left = PWMOutputDevice(23)
motor_right = PWMOutputDevice(24)

# Path of song file (.csv) - must be located in the project directory
song_path = "song.csv"

# Set tempo
bpm = 260
tick = 60.0 / float(bpm)

# Play the song
playSong(song_path, tick)