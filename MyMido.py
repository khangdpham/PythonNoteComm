import mido
import time
import argparse
import signal
import sys
import threading
import random

from neopixel import *

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
SHIFT_KEY      = 9

class MusicLightning(object):
  def __init__(self,interval=1):
    self.autoShow = []
    self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    self.strip.begin()
    autoThread = threading.Thread(target=self.auto_lightshow,)
    autoThread.start()
    ariusThread = threading.Thread(target=self.run)
    pipeF= threading.Thread(target=self.pipeFlush)
    ariusThread.start()
    pipeF.start()

  def pipeFlush(self):
    while True:
      if len(self.autoShow) > 0:
        self.autoShow.pop(0)
      time.sleep(1)
  def run(self):
    while True:
        print(mido.get_input_names())
        with mido.open_input('ARIUS MIDI 1') as inport:
          for msg in inport:
            if msg.type == 'note_on':
              arr=str(msg).split(" ")
              note=int(arr[2].split('=')[1]) -  SHIFT_KEY
              velocity=int(arr[3].split('=')[1])
              print(note," : ",velocity)
              if velocity == 0:
                self.strip.setPixelColor(note,Color(0,0,0))
              else:
                if (len(self.autoShow)< 20):
                  self.autoShow.append(note)
                self.strip.setPixelColor(note,Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
              self.strip.show()
  def auto_lightshow(self):
    while True: 
      print(len(self.autoShow))
      if len(self.autoShow) > 0 :
        time.sleep(1)
        continue
      else: 
        randomColor = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        rcase = random.randint(0,10)
        if rcase%5 == 0:
          self.colorWipe(self.strip,randomColor)
        if rcase%5 == 1:
          self.theaterChase(self.strip,randomColor,100)
        if rcase%5 == 2:
          self.rainbow(self.strip)
        if rcase%5 == 3:
          self.swift(self.strip)
        self.ClearAll(self.strip)
  def ClearAll(self,strip):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i,Color(0,0,0))
    strip.show()
  def swift(self,strip):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i,Color(random.randint(10,255),random.randint(10,255),random.randint(10,255)))
      strip.show()
      time.sleep(0.005)
    for i in range(strip.numPixels(),-1,-1):
      strip.setPixelColor(i,0)
    strip.show()
    for i in range(strip.numPixels(),-1,-1):
      strip.setPixelColor(i,Color(random.randint(10,255),random.randint(10,255),random.randint(10,255)))
      strip.show()
      time.sleep(0.005)
    time.sleep(0.01)
    for i in range(strip.numPixels(),-1,-1):
      strip.setPixelColor(i,0)
    strip.show()
 
  def signal_handler(signal, frame):
    colorWipe(strip, Color(0,0,0))
    sys.exit(0)
  
  def wheel(self,pos):
    if pos < 85:
      return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
      pos -= 85
      return Color(255 - pos * 3, 0, pos * 3)
    else:
      pos -= 170
      return Color(0, pos * 3, 255 - pos * 3)

  def rainbow(self,strip, wait_ms=20, iterations=1):
    for j in range(256*iterations):
      for i in range(strip.numPixels()):
        strip.setPixelColor(i,self.wheel((i+j) & 255))
      strip.show()
      time.sleep(wait_ms/1000.0)
  def colorWipe(self,strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, color)
      strip.show()
      time.sleep(wait_ms/1000.0)

  def theaterChase(self,strip, color, wait_ms=50, iterations=10):
    for j in range(iterations):
      for q in range(3):
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, 0)
# Main program logic follows:
if __name__ == '__main__':
  ml = MusicLightning()
