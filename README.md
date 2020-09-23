# DashZero
[![Version](https://img.shields.io/badge/version-alpha-red.svg?style=for-the-badge)](#) [![mantained](https://img.shields.io/maintenance/yes/2020.svg?style=for-the-badge)](#)

[![maintainer](https://img.shields.io/badge/maintainer-Goran%20Zunic%20%40panbachi-blue.svg?style=for-the-badge)](https://www.panbachi.de)

# !!!WARNING!!!
DashZero is currently an early alpha. Everything could be changed in future.

# Introduction
DashZero is a small customizable smart-home dashboard for (but not only) the Raspberry Pi Zero. The idea was to run a Home-Assistant UI on the SHPI.zero (which uses a Raspberry Pi Zero). As the Raspberry Pi Zero is too slow to run the Home-Assistant UI in a browser, I decided to write my own UI.

As everything else, also this project is aging. So before only Home-Assistant was integrated in DashZero. In this version also ioBroker has a bit of compatibility. For more informations scroll down!

The current version only works with the SHPI.one device and the official QT-Image or with Raspberrie Pi's running QT >= 5.12.

# Features
DashZero is fully (or will be) customizable. You can configure it by simply change the config.yaml file.

You can define multiple room. Rooms are a collection of multiple cards. Currently the following cards are available:

- Weather
- Door
- Thermostat
- Entities
- EntitesGrid

For now DashZero only works with Home-Assistant and ioBroker, but its prepared to add other home automation connectors for example MQTT, openHAB or even FHEM. But feel free to add any connector you like.

# Instalation
## Requirements
- for now only the SHPI.one with the QT-Image or an Raspberry Pi with QT > 5.12

## Install dependencies
```
python3 -m pip install pyyaml
python3 -m pip install websocket_client
python3 -m pip install dateparser
(and perhaps some more :)...)
```

## Configure DashZero
Copy `config.example.yaml` to `config.yaml` and edit the `config.yaml` file to fit your needs.
Look at the `config.yaml` to see what happens. If you don't understand anything, so wait for the final release of the docs :)

### Home-Assistant
#### Currently supported:
- Weather
- Door
- Thermostat (partially, could not control devices)
- Entities
- EntitesGrid

##### Configuration
Add the Home-Assistant connector to your config.yaml

```
connectors:
  homeassistant:
    host: HOST
    port: 8123
    access_token: "ACCESS_TOKEN"
```

Replace `HOST` and `ACCESS_TOKEN` with your host and access token.

#### Weather
To add the weather card to your room, add the following code to your room:

```
rooms:
  ...
    cards:
      ...
      - type: weather
        name: Home-Assistant
        connector: homeassistant
        entity_id: weather.home
      ...
```

#### Entities and Entities-Grid
To add the entities or entites-grid card to your room, add the following code to your room:

```
rooms:
  ...
    cards:
      - type: entities
        name: Home-Assistant
        entities:
          - name: ENTITY_NAME
            connector: homeassistant
            entity_id: sensor.ENTITY_ID
            type: sensor
            icon: "clock"
          - name: ENTITY_NAME
            connector: homeassistant
            entity_id: switch.ENTITY_ID
            type: switch
            icon: "clock"
          - name: ENTITY_NAME
            connector: homeassistant
            entity_id: light.ENTITY_ID
            type: switch
            icon: "clock"
```

For a grid-view replace `entities` with `entities-grid`.

Supported types are for now `switch` and `sensor`. But Home-Assistant `light` entities could be turned on and of if you config them as `switch`. 

`ENTITY_ID` could be something like: `light.zigbee_light_1` or `sensor.thermostat_temperature` or `switch.ac`.

#### Door
To add the door to your room, add the following code to your room:

```
rooms:
  ...
    cards:
      - type: door
        name: Home-Assistant
        opener:
          connector: homeassistant
          entity_id: switch.ENTITY_ID
        camera:
          connector: homeassistant
          entity_id: camera.ENTITY_ID
```

Your opener `ENTITY_ID` should a switch entity and your camera `ENTITY_ID` should be a camera entity.

#### Thermostat
To add the thermostat to your room, add the following code to your room:

```
rooms:
  ...
    cards:
      - type: thermostat
        name: Home-Assistant
        connector: homeassistant
        entity_id: climate.ENTITY_ID
        sensors:
          - name: Temperature
            connector: homeassistant
            entity_id: sensor.ENTITY_ID
            icon: "thermometer"
          - name: Battery
            connector: homeassistant
            entity_id: sensor.ENTITY_ID
            icon: "battery"
        controls:
          - type: temperature
            value: 30
            icon: fire
            color: "#E74C3C"
          - type: temperature
            value: 4
            icon: snowflake
            color: "#3498DB"
```

Your card-entity_id must be an `climate` entity. You could add as many sensors as you want to the `sensors` list. `controls` have currently no effect.

### ioBroker
#### Currently supported:
- Weather
- Door (partially, could not show camera)
- Thermostat (partially, could not control devices and could not show etched temperature)
- Entities
- EntitesGrid

##### Configuration
Add the ioBroker connector to your config.yaml

```
connectors:
  iobroker:
    host: HOST
    port: 8084
```

Replace `HOST` with your host.

#### Weather
To add the weather-card to your room add the following code to your room:

```
rooms:
  ...
    cards:
      - type: weather
        name: ioBroker
        connector: iobroker
        entity_id: openweathermap.0
```

The weather card currently only works with the OpenWeatherMap-Adapter.

It is important to add the object ID of the `openweathermap.x` object as shown in the example.

#### Entities and Entities-Grid
To add the entities or entites-grid card to your room, add the following code to your room:

```
rooms:
  ...
    cards:
      - type: entities
        name: ioBroker
        entities:
          - name: ENTITY_NAME
            connector: iobroker
            entity_id: ENTITY_ID
            type: sensor
            icon: "clock"
          - name: ENTITY_NAME
            connector: iobroker
            entity_id: ENTITY_ID
            type: switch
            icon: "clock"
          - name: ENTITY_NAME
            connector: iobroker
            entity_id: ENTITY_ID
            type: switch
            icon: "clock"
```

For a grid-view replace `entities` with `entities-grid`.

Supported types are for now `switch` and `sensor`.

Type `sensor` in the config could be (afaik) any type in ioBroker.
Type `switch` in the config should be type `switch` in ioBroker.

#### Door
To add the door to your room, add the following code to your room:

```
rooms:
  ...
    cards:
      - type: door
        name: ioBroker
        opener:
          connector: ioBroker
          entity_id: ENTITY_ID
        camera:
          connector: homeassistant
          entity_id: camera.ENTITY_ID
```

Your `opener` `ENTITY_ID` should a switch entity. `camera` is currently not supported for ioBroker. 

#### Thermostat
To add the thermostat to your room, add the following code to your room:

```
rooms:
  ...
    cards:
      - type: thermostat
        name: Home-Assistant
        connector: homeassistant
        entity_id: climate.ENTITY_ID
        sensors:
          - name: Temperature
            connector: iobroker
            entity_id: ENTITY_ID
            icon: "thermometer"
          - name: Battery
            connector: iobroker
            entity_id: ENTITY_ID
            icon: "battery"
        controls:
          - type: temperature
            value: 30
            icon: fire
            color: "#E74C3C"
          - type: temperature
            value: 4
            icon: snowflake
            color: "#3498DB"
```

Currently only `sensor` entities are supported. That could be (afaik) any type in ioBroker.


### Start DashZero
`python3 main.py`

# Support me / Follow me
[![Web](https://img.shields.io/badge/www-panbachi.de-blue.svg?style=flat-square&colorB=3d72a8&colorA=333333)](https://www.panbachi.de)
[![Facebook](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=facebook&colorB=3B5998&colorA=333333)](https://www.facebook.com/panbachi.de/)
[![Twitter](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=twitter&colorB=1DA1F2&colorA=333333)](https://twitter.com/panbachi)
[![Instagram](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=instagram&colorB=E4405F&colorA=333333)](http://instagram.com/panbachi.de)
[![YouTube](https://img.shields.io/badge/-%40panbachi.de-blue.svg?style=flat-square&logo=youtube&colorB=FF0000&colorA=333333)](https://www.youtube.com/channel/UCO7f2L7ZsDCpOtRfKnPqNow)
