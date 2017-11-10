#!/usr/bin/python

import paho.mqtt.client as mqtt
import time
import json
from jsonschema import validate
from jsonschema import exceptions
from uuid import getnode as get_mac
from lib.neo_pixel_string import *
from random import *

# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
BROKER_ADDRESS = "10.0.0.100"        # broker.mqttdashboard.com
BROKER_PORT = 1883                 # 1883
QOS_STATE_PUBLISH = 1
    # At most once (0)
    # At least once (1)
    # Exactly once (2)
RETAIN_STATE_PUBLISH = True

loopflag = False
animation = 'none'

full_state_schema = {
    "type" : "object",
    "properties" : {
        "state" : {"enum" : ["ON", "OFF"]},
        "effect" : {"enum" : ["rainbow", "rainbowcycle", "theaterchaserainbow", "colorwipe", "theaterchase"]},
        "brightness" : {"type": "number", "minimum": 0, "maximum": 255 },
        "color": {
            "type" : "object",
            "properties" : {
                "r" : {"type": "number", "minimum": 0, "maximum": 255 },
                "g" : {"type": "number", "minimum": 0, "maximum": 255 },
                "b" : {"type": "number", "minimum": 0, "maximum": 255 }
            },
            "required": ["r", "g", "b"]
        }
    }
}

neopixelstring = None

def on_connect(client, userdata, flags, rc):
    m = "Connected flags" + str(flags) + "result code " \
        + str(rc) + "client1_id " + str(client)
    print(m)

# This is an interface that is compatible with Home Assistant MQTT JSON Light
def on_message_full_state(client, userdata, message):
    global json_message, loopflag, animation
    json_message = str(message.payload.decode("utf-8"))
    print("message received: ", json_message)

    try:
        data = json.loads(json_message)
        validate(data, full_state_schema)
        if (data.has_key('state')):
            if (data['state'] == 'ON'):
                neopixelstring.all_on()
            else:
                neopixelstring.all_off()

        if (data.has_key('brightness')):
            neopixelstring.set_brightness(data['brightness'])

        if (data.has_key('color')):
            # For some reason we need to switch r and g. Don't get it
            color = Color(data['color']['g'], data['color']['r'], data['color']['b'])
            neopixelstring.set_color(color)

        if (data.has_key('effect')):
            loopflag = True
            if (data['effect'] == 'rainbow'):
               animation = 'rainbow'
            elif (data['effect'] == 'rainbowcycle'):
               animation = 'rainbowcycle'
            elif (data['effect'] == 'theaterchaserainbow'):
               animation = 'theaterchaserainbow'
            elif (data['effect'] == 'colorwipe'):
               animation = 'colorwipe'
            elif (data['effect'] == 'theaterchase'):
               animation = 'theaterchase'
        else:
            animation = 'none'
            loopflag = False

        publish_state(client)

    except exceptions.ValidationError:
        print "Message failed validation"
    except ValueError:
        print "Invalid json string"

def publish_state(client):
    json_state = {
        "brightness": neopixelstring.get_brightness(),
        "state": "OFF" if neopixelstring.is_off() else "ON",
        "color": {
            "r": neopixelstring.get_color()['red'],
            "g": neopixelstring.get_color()['green'],
            "b": neopixelstring.get_color()['blue']
        }
    }

    (status, mid) = client.publish("saito/bed/neopixels", json.dumps(json_state), \
        QOS_STATE_PUBLISH, RETAIN_STATE_PUBLISH)

    if status != 0:
        print("Could not send state")

# Main program logic follows:
if __name__ == '__main__':
    neopixelstring = NeoPixelString(LED_COUNT, LED_PIN)
    mac = get_mac()

    client1 = mqtt.Client(str(mac) + "-python_client")
    client1.on_connect = on_connect

    # Home Assistant compatible
    client1.message_callback_add("saito/bed/neopixels/set", on_message_full_state)
    time.sleep(1)

    client1.connect(BROKER_ADDRESS, BROKER_PORT)
    client1.loop_start()
    client1.subscribe("saito/bed/neopixels/set")

    justoutofloop = False
    print ('Press Ctrl-C to quit.')
    while True:
        if loopflag and animation != 'none':
            if animation == 'rainbow':
                neopixelstring.rainbow()
            elif (animation == 'rainbowcycle'):
               neopixelstring.rainbowCycle()
            elif (animation == 'theaterchaserainbow'):
               neopixelstring.theaterChaseRainbow()
            elif (animation == 'colorwipe'):
               neopixelstring.colorWipe(Color(randint(0,255), randint(0,255), randint(0,255)))
        if not loopflag and justoutofloop:
            justoutofloop = False
            client1.publish("saito/bed/neopixels/set", json_message, 0, False)
        time.sleep(.1)

    # This should happen but it doesnt because CTRL-C kills process.
    # Fix later
    print "Disconnecting"
    publish_state(client1)
    client1.disconnect()
    client1.loop_stop()
