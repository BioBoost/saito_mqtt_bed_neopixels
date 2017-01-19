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

## Mqtt

Currently script uses http://www.mqtt-dashboard.com/ as mqtt broker. Should be changed to our own broker later.

### Neopixel color topic

Actual topic is `saito/bed/neopixels/color` and it expects a json string of following format:

```json
{
  "red": 0,
  "green": 0,
  "blue": 0
}
```
where red, green and blue are values between 0 and 255.

### Neopixel brightness

Actual topic is `saito/bed/neopixels/brightness` and it expects a json string of following format:

```json
{
  "brightness": 0
}
```
where brightness is value between 0 and 255.
