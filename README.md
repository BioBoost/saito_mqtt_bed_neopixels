# Saito MQTT NeoPixel Bed

Very simple mqtt client app in Python that allows control of NeoPixel ring
attached to the my kids bed.

Makes use of Jeremy Garffs neopixel lib for the Rpi. More info at:

* https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all
* https://github.com/jgarff/rpi_ws281x

## Installing rpi_ws281x

```shell
sudo apt-get update
sudo apt-get install build-essential python-dev git scons swig
cd ; git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install
```

## Other requirements

You also need jsonschema and paho mqtt libs.

```shell
sudo pip install jsonschema
sudo pip install paho-mqtt
```

## Hardware

Currently library defaults to GPIO18 (pin 12) on http://www.raspberry-pi-geek.com/howto/GPIO-Pinout-Rasp-Pi-1-Model-B-Rasp-Pi-2-Model-B

## Home Assistant

Just add an MQTT JSON Light with following config:

```
# Enable mqtt
mqtt:
  broker: xxxxxxxxxxxxx
  port: 8000
  client_id: xxxxxxxxxxxxxxxxx
  keepalive: 60

# Example configuration.yaml entry
light:
  platform: mqtt_json
  name: "Saito RGB Light"
  command_topic: "saito/bed/neopixels/set"
  state_topic: "saito/bed/neopixels"
  brightness: true
  rgb: true
```

and you are good to go.

State and commands are passed using json:

```json
{
  "brightness": 255,
  "color": {
    "g": 255,
    "b": 255,
    "r": 255
  },
  "transition": 2,
  "state": "ON"
}
```

## Autostart on Raspberry Pi

Just use pm2 to start the script

```shell
sudo su
pm2 startup
pm2 start app.py --name saito_bed_neopixels
pm2 save
```
