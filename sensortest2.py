#!/usr/bin/python

#arguments to turn lights on and off: LED_COUNT, BRIGHTNESS, R, G, B, W, on time, off time,outFile, checkTime)

import sys
import time
from neopixel import *
import Adafruit_MCP9808.MCP9808 as MCP9808
from tentacle_pi.TSL2561 import TSL2561
import csv
import RPi.GPIO as GPIO


sys.path.append("/home/pi/SHT31_PAE")
from SHT31 import *

#set up IR lights
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

print 'Argument List:', str(sys.argv)

R=int(sys.argv[3])
G=int(sys.argv[4])
B=int(sys.argv[5])
W=int(sys.argv[6])
onTime=int(sys.argv[7])
offTime=int(sys.argv[8])
outFile=str(sys.argv[9])
checkTime=float(sys.argv[10])

#set up light moniter
tsl = TSL2561(0x39,"/dev/i2c-1")
tsl.enable_autogain()
tsl.set_time(0x00)


LED_COUNT      = int(sys.argv[1])   # Number of LED pixels.
LED_PIN        = 18                 # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000             # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5                  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = int(sys.argv [2])  # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False              # True to invert the signal (when using NPN transistor
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812_STRIP_RGBW	


# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

# Intialize the library (must be called once before other functions).
strip.begin()

#Turn on temperature sensor
sensor = MCP9808.MCP9808()

sensor.begin()

#make a datafile
c =(open(outFile, 'wb'))
wrtr = csv.writer(c)
wrtr.writerow(["TimeStamp", "MCP9808Temp", "SHT31Temp", "Humidity", "Lux", "Lights"])

#start checking the time
while True:
    #what time is it?
    now= time.localtime(time.time())
    timeStamp=time.strftime("%y-%m-%d %H:%M:%S", now)
    print timeStamp
    #apply calculation to time
    minute= int(time.strftime("%S"))
    #read MCP9808 sensor
    currtemp=sensor.readTempC()
    print "MCP9808 Temperature is", currtemp
    SHT31reading=read_SHT31()
    print "SHT31 Temperature is", SHT31reading[0]
    print "SHT31 Humidity is", SHT31reading[1]
    #read light sensor
    currlux=tsl.lux()
    print "Lux is", currlux
    print 
    if onTime <= minute % 10 <offTime:
        print ' Lights on! LED On!'
        lights=True
        GPIO.output(16,True)
        for i in range(LED_COUNT):
            strip.setPixelColor(i,Color(R,G,B,W))
            strip.show()
            time.sleep(.1)
    else:
        print 'Lights off!, LED Off!'
        GPIO.output(16,False)
        lights=False
        for i in range(LED_COUNT):
            strip.setPixelColor(i,Color(0,0,0,0))
            strip.show()
            time.sleep(.1)
    wrtr.writerow([timeStamp,currtemp, SHT31reading[0], SHT31reading[1], currlux, lights])
    c.flush()
    time.sleep(checkTime)
