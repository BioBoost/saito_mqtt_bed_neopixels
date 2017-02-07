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
	ON, OFF = range(2)

	def __init__(self, numberOfLeds, pin):
		self.numberOfLeds = numberOfLeds
		self.color = Color(255, 255, 255)
		self.brightness = NeoPixelString.DEFAULT_BRIGHTNESS

		self.strip = Adafruit_NeoPixel(numberOfLeds, pin,	\
			NeoPixelString.LED_FREQ_HZ, NeoPixelString.LED_DMA, \
			NeoPixelString.LED_INVERT, self.brightness)

		# Intialize the library (must be called once before other functions).
		self.strip.begin()
		self.all_off()

	def set_color(self, color):
		self.color = color
		for i in range(0, self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
		self.strip.show()

	def all_off(self):
		keep_color = self.color
		self.set_color(Color(0, 0, 0))
		self.color = keep_color
		self.state = NeoPixelString.OFF

	def all_on(self):
		self.set_color(self.color)
		self.state = NeoPixelString.ON

	def set_brightness(self, brightness):
		self.brightness = brightness
		self.strip.setBrightness(brightness)
		self.set_color(self.color)

	def get_brightness(self):
		return self.brightness

	def get_color(self):
		# Red and green seem te be reversed for some reason
		blue = self.color % 256
		red = (self.color >> 8) % 256
		green = (self.color >> 16) % 256
		return { 'red': red, 'green': green, 'blue': blue }

	def is_off(self):
		return self.state == NeoPixelString.OFF

	def is_on(self):
		return (not self.is_off())
