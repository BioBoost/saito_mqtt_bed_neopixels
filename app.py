import time

import paho.mqtt.client as mqtt
import time
import json
from jsonschema import validate
from jsonschema import exceptions
from uuid import getnode as get_mac
from lib.neo_pixel_string import *

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).


brightness_schema = {
    "type" : "object",
    "properties" : {
    	"brightness" : {"type": "number"}
	},
    "required": ["brightness"]
}

color_schema = {
    "type" : "object",
    "properties" : {
        "red" : {"type" : "number"},
	    "green" : {"type" : "number"},
		"blue" : {"type" : "number"}
    },
    "required": ["red", "green", "blue"]
}

neopixelstring = None


def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id  "+str(client)
    print(m)

# {"red":255, "green":96, "blue":5}
def on_message_color(client, userdata, message):
	json_message = str(message.payload.decode("utf-8"))
	print("message received: ", json_message)

	try:
		data = json.loads(json_message)
		validate(data, color_schema)
		color = Color(data['green'], data['red'], data['blue'])
		neopixelstring.set_color(color)
	except exceptions.ValidationError:
		print "Message failed validation"
	except ValueError:
		print "Invalid json string"

# {"brightness": 80}
def on_message_brightness(client, userdata, message):
	json_message = str(message.payload.decode("utf-8"))
	print("message received: ", json_message)

	try:
		data = json.loads(json_message)
		validate(data, brightness_schema)
		neopixelstring.set_brightness(data['brightness'])
	except exceptions.ValidationError:
		print "Message failed validation"
	except ValueError:
		print "Invalid json string"

# Main program logic follows:
if __name__ == '__main__':
	neopixelstring = NeoPixelString(LED_COUNT, LED_PIN)

	mac = get_mac()

	broker_address="broker.mqttdashboard.com"

	client1 = mqtt.Client(str(mac) + "-python_client")    #create new instance
	client1.on_connect = on_connect        #attach function to callback
	# client1.on_message = on_message        #attach function to callback

	client1.message_callback_add("saito/bed/neopixels/color", on_message_color)
	client1.message_callback_add("saito/bed/neopixels/brightness", on_message_brightness)

	time.sleep(1)

	client1.connect(broker_address)      #connect to broker
	client1.loop_start()    #start the loop
	client1.subscribe("saito/bed/neopixels/color")
	client1.subscribe("saito/bed/neopixels/brightness")
	# client1.publish("bioboost/temperature","12.33")

	# time.sleep(5)

	print ('Press Ctrl-C to quit.')
	while True:
		time.sleep(1)
		# # Color wipe animations.
		# colorWipe(strip, Color(255, 0, 0))  # Red wipe
		# colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		# colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# # Theater chase animations.
		# theaterChase(strip, Color(127, 127, 127))  # White theater chase
		# theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		# theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# # Rainbow animations.
		# rainbow(strip)
		# rainbowCycle(strip)
		# theaterChaseRainbow(strip)



	client1.disconnect()
	client1.loop_stop()
