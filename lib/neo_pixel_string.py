# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
# https://github.com/jgarff/rpi_ws281x
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from neopixel import *

class NeoPixelString:
	# LED strip configuration:
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	DEFAULT_BRIGHTNESS = 20

	def __init__(self, numberOfLeds, pin):
		self.numberOfLeds = numberOfLeds

		self.strip = Adafruit_NeoPixel(numberOfLeds, pin,	\
			NeoPixelString.LED_FREQ_HZ, NeoPixelString.LED_DMA, \
			NeoPixelString.LED_INVERT, NeoPixelString.DEFAULT_BRIGHTNESS)

		# Intialize the library (must be called once before other functions).
		self.strip.begin()
		self.all_off()

	def set_color(self, color):
		for i in range(0, self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
		self.strip.show()

	def all_off(self):
		self.set_color(Color(0, 0, 0))

	def set_brightness(self, brightness):
		self.strip.setBrightness(brightness)
