# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
# https://github.com/jgarff/rpi_ws281x
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from neopixel import *
import time

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

	global wheel
	def wheel(pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256*iterations):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, wheel((i+j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)

        def rainbowCycle(self, wait_ms=20, iterations=5):
                """Draw rainbow that uniformly distributes itself across all pixels."""
                for j in range(256*iterations):
                        for i in range(self.strip.numPixels()):
                                self.strip.setPixelColor(i, wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
                        self.strip.show()
                        time.sleep(wait_ms/1000.0)

	def theaterChaseRainbow(self, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			for q in range(3):
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, wheel((i+j) % 255))
				self.strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, 0)

	def colorWipe(self, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		self.color = color
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChase(self, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		self.color = color
		for j in range(iterations):
			for q in range(3):
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, color)
				self.strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, 0)

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
