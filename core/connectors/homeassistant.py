import json
import websocket
import threading
import dateparser
from core.storage import Storage
from PySide2.QtCore import Slot

class HomeAssistant(object):
    def __init__(self, config):
        self.config = config
        self.message_count = 2

        self.cardinal_directions = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
            "N",
        ]

        self.weather_icons = {
            "clear-night": "weather-night",
            "cloudy": "weather-cloudy",
            "exceptional": "alert-circle-outline",
            "fog": "weather-fog",
            "hail": "weather-hail",
            "lightning": "weather-lightning",
            "lightning-rainy": "weather-lightning-rainy",
            "partlycloudy": "weather-partly-cloudy",
            "pouring": "weather-pouring",
            "rainy": "weather-rainy",
            "snowy": "weather-snowy",
            "snowy-rainy": "weather-snowy-rainy",
            "sunny": "weather-sunny",
            "windy": "weather-windy",
            "windy-variant": "weather-windy-variant",
        }

        self.weather_labels = {
            "clear-night": "Klare Nacht",
            "cloudy": "Bewölkt",
            "fog": "Nebel",
            "hail": "Hagel",
            "lightning": "Gewitter",
            "lightning-rainy": "Gewitter, regnerisch",
            "partlycloudy": "Teilweise bewölkt",
            "pouring": "Strömend",
            "rainy": "Regnerisch",
            "snowy": "Verschneit",
            "snowy-rainy": "Verschneit, regnerisch",
            "sunny": "Sonnig",
            "windy": "Windig",
            "windy-variant": "Windig",
            "exceptional": "Außergewöhnlich"
        }

        self.weekdays = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa']

    def start(self):
        websocket.enableTrace(False)
        url = "ws://" + self.config['host'] + ":" + str(self.config['port']) + '/api/websocket'
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)

        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def init_entities(self, data):
        for result in data['result']:
            self.on_state_changed({'entity_id': result['entity_id'], 'new_state': result})

    def wind_bearing_to_text(self, degree):
        return self.cardinal_directions[int((int((int(degree) + 11.25) / 22.5) | 0) % 16)]

    def on_state_changed(self, data):
        entity = Storage.instance().entities().get('homeassistant', data['entity_id'])

        if entity:
            for entity_type in entity:

                state = {
                    'entity_id': data['entity_id']
                }

                if 'unit_of_measurement' in data['new_state']['attributes']:
                    state['unit'] = data['new_state']['attributes']['unit_of_measurement']


                if 'state' in data['new_state'] and data['new_state']['state'] != 'unknown':
                    state['state'] = data['new_state']['state']
                elif 'temperature' in data['new_state']['attributes']:
                    state['state'] = data['new_state']['attributes']['temperature']

                key = data['entity_id'].split('.')[0]
                if key == 'camera':
                    state['picture'] = 'http://' + self.config['host'] + ':' + self.config['port'] + data['new_state']['attributes']['entity_picture']

                if key == 'weather':
                    state['condition_icon'] = self.weather_icons[data['new_state']['state']]
                    state['condition_label'] = self.weather_labels[data['new_state']['state']]
                    state['temperature'] = data['new_state']['attributes']['temperature']
                    state['humidity'] = data['new_state']['attributes']['humidity']
                    state['pressure'] = data['new_state']['attributes']['pressure']
                    state['wind_speed'] = data['new_state']['attributes']['wind_speed']
                    state['wind_direction'] = self.wind_bearing_to_text(data['new_state']['attributes']['wind_bearing'])
                    state['forecast'] = []


                    for forecast in data['new_state']['attributes']['forecast']:
                        state['forecast'].append({
                            'day': self.weekdays[dateparser.parse(forecast['datetime']).weekday()],
                            'condition_icon': self.weather_icons[forecast['condition']],
                            'temperature': forecast['temperature']
                        })

                Storage.instance().entities().changeState(
                    'homeassistant',
                    data['entity_id'],
                    entity_type,
                    state)



    def on_message(self, message):
        message = json.loads(message)

        if message['type'] == 'result' and message['id'] == 2:
            self.init_entities(message)

        if message['type'] == 'event':
            self.on_state_changed(message['event']['data'])

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        self.ws.send(json.dumps(
            {'type': 'auth',
             'access_token': self.config['access_token']}
        ))

        self.ws.send(json.dumps(
            {'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}
        ))

        self.ws.send(json.dumps(
            {'id': 2, 'type': 'get_states'}
        ))

    @Slot()
    def setState(self, entity_id, entity_type, value):
        if entity_type == 'switch':
            self.message_count = self.message_count + 1
            service = 'turn_' + value
            domain = entity_id.split('.')[0]
            self.ws.send(json.dumps({
                "id": self.message_count,
                "type": "call_service",
                "domain": domain,
                "service": service,
                "service_data": {
                    "entity_id": entity_id
                }
            }))
