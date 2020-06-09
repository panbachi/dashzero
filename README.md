# DashZero
[![Version](https://img.shields.io/badge/version-alpha-red.svg?style=for-the-badge)](#) [![mantained](https://img.shields.io/maintenance/yes/2020.svg?style=for-the-badge)](#)

[![maintainer](https://img.shields.io/badge/maintainer-Goran%20Zunic%20%40panbachi-blue.svg?style=for-the-badge)](https://www.panbachi.de)

**!!!WARNING!!!** dashzero is currently an early alpha. Everything could be changed in future.


dashzero is a small customizable smart home dashboard for (but not only) the Raspberry Pi Zero. The idea was to run a home-assistant UI on the SHPI.zero (which uses a Raspberry Pi Zero). As the Raspberry Pi Zero is too slow to run the home-assistant UI in a browser, I decided to write my own UI.

## Features
dashzero is fully (or will be) customizable. You can configure it by simply change the config.yaml file.

You can define multiple room. Rooms are a collection of multiple cards. Currently the following cards are available:

- Weather
- Door
- Garbage
- Thermostat
- Lights

For now dashzero only works with home-assistant, but its prepared to add other home automation connectors for example to ioBroker, openHAB or even MQTT.

## Installation
### Requirements
- Raspberry Pi OS (previously called Raspbian)
- If you use SHPI follow the instructions on: https://github.com/shpi/zero_setup

### Install dependecies
```
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev

python3 -m pip install --upgrade --user pip setuptools
python3 -m pip install --upgrade --user Cython==0.29.10 pillow
python3 -m pip install --user kivy
python3 -m pip install kivymd
python3 -m pip install pyyaml
python3 -m pip install Twisted
python3 -m pip install autobahn[twisted]
```

### Configure Kivy
Edit file `/home/pi/.kivy/config.ini`

Make sure, the following settings are set as described:

```
[graphics]
height = 480
show_cursor = 0
borderless = 1

[input]
mouse = mouse
%(name)s = probesysfs,provider=hidinput,param=invert_y=0
```

### Configure DashZero
Copy `config.example.yaml` to `config.yaml` and edit the `config.yaml` file to fit your needs. A description how to configure DashZero in detail will follow soon.


# Support me / Follow me
[![Web](https://img.shields.io/badge/www-panbachi.de-blue.svg?style=flat-square&colorB=3d72a8&colorA=333333)](https://www.panbachi.de)
[![Facebook](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=facebook&colorB=3B5998&colorA=333333)](https://www.facebook.com/panbachi.de/)
[![Twitter](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=twitter&colorB=1DA1F2&colorA=333333)](https://twitter.com/panbachi)
[![Instagram](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=instagram&colorB=E4405F&colorA=333333)](http://instagram.com/panbachi.de)
[![YouTube](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=youtube&colorB=FF0000&colorA=333333)](https://www.youtube.com/channel/UCO7f2L7ZsDCpOtRfKnPqNow)
