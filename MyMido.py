import mido
import time

from neopixel import *

import argparse
import signal
import sys
import threading

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
SHIFT_KEY      = 21
class MusicLightning(object):
  def __init__(self,interval=1):
    self.run()

    #self.interval = interval
    #thread=threading.Thread(target=self.run,args=())
    #thread.daemon = True
    #thread.start()
  def run(self):
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()

    print(mido.get_input_names())
    with mido.open_input('ARIUS MIDI 1') as inport:
      for msg in inport:
        if msg.type == 'note_on':
          arr=str(msg).split(" ")
          note=int(arr[2].split('=')[1]) - SHIFT_KEY
          velocity=int(arr[3].split('=')[1])
          print(note," : ",velocity)
          print(note," : ",velocity)
          if velocity == 0:
            strip.setPixelColor(note,Color(0,0,0))
          else:
            strip.setPixelColor(note,Color(255,128,0))
          strip.show()
          print("Ending")
  def signal_handler(signal, frame):
    colorWipe(strip, Color(0,0,0))
    sys.exit(0)

  def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, color)
      strip.show()
      time.sleep(wait_ms/1000.0)

  def theaterChase(strip, color, wait_ms=50, iterations=10):
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
