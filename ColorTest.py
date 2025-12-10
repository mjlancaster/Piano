import time
import board
import adafruit_tcs34725
import math
from gpiozero import LED

# Normalize Vector
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

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

colors_name = ["red", "green", "pink", "yellow", "blue"]
colors_RGB = [[20, 5, 5], [8, 10, 5], [12, 5, 5], [33, 23, 9], [4, 4, 4]]
colors_RGB_norm = []

led = LED(16)

for item in colors_RGB:
    colors_RGB_norm.append(normalize(item))
    

while True:
    r,g,b,c = sensor.color_raw
    guess = guessColor(r, g, b, colors_RGB_norm)
    if (guess == 1):
        led.on()
    else:
        led.off()
    print("guess: ", colors_name[guess], " r: ", r, " g ", g, " b: ", b)
