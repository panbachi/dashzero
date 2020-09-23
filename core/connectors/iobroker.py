import socketio
from datetime import datetime
from core.storage import Storage
from PySide2.QtCore import QObject, Slot, QTimer

class IoBroker(socketio.Client):
    def __init__(self, config):
        socketio.Client.__init__(self)
        self.entities = {}
        self.config = config

        self.weather_icons = {
            "https://openweathermap.org/img/w/01d.png": "weather-sunny",
            "https://openweathermap.org/img/w/01n.png": "weather-night",
            "https://openweathermap.org/img/w/02d.png": "weather-partly-cloudy",
            "https://openweathermap.org/img/w/02n.png": "weather-partly-cloudy",
            "https://openweathermap.org/img/w/03d.png": "weather-cloudy",
            "https://openweathermap.org/img/w/03n.png": "weather-cloudy",
            "https://openweathermap.org/img/w/04d.png": "weather-cloudy",
            "https://openweathermap.org/img/w/04n.png": "weather-cloudy",
            'https://openweathermap.org/img/w/09d.png': 'weather-rainy',
            'https://openweathermap.org/img/w/09n.png': 'weather-rainy',
            'https://openweathermap.org/img/w/10d.png': 'weather-rainy',
            'https://openweathermap.org/img/w/10n.png': 'weather-rainy',
            'https://openweathermap.org/img/w/11d.png': 'weather-lightning',
            'https://openweathermap.org/img/w/11n.png': 'weather-lightning',
            "https://openweathermap.org/img/w/13d.png": "weather-snowy",
            "https://openweathermap.org/img/w/13n.png": "weather-snowy",
            "https://openweathermap.org/img/w/50d.png": "weather-fog",
            "https://openweathermap.org/img/w/50n.png": "weather-fog",
        }

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

        self.weekdays = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa']

    def start(self):

        try:
            self.connect('http://' + self.config['host'] + ':' + str(self.config['port']), headers={
                'query': 'key=nokey'
            }, namespaces=['vis.0'])
        except Exception as e:
            pass

    def _handle_connect(self, namespace):
        super()._handle_connect(namespace)
        print('connection established')
        self.emit('name', 'vis.0')
        self.emit('authenticate', callback=self.authenticate)

    def _handle_event(self, namespace, id, data):
        super()._handle_event(namespace, id, data)

        if data[0] == 'stateChange':
            self.on_state_change(data[1], data[2])

    def authenticate(self, isOk, isSecure):
        self.emit('subscribe', '*')
        self.emit('getObjects', callback=self.init_objects)

    def wind_bearing_to_text(self, degree):
        return self.cardinal_directions[int((int((int(degree) + 11.25) / 22.5) | 0) % 16)]

    def on_state_change(self, entity, data):
        if not data:
            return
        if entity in self.entities:
            original_entity = entity

            if entity.startswith('openweathermap.'):
                parts = entity.split('.')
                entity = parts[0] + '.' + parts[1]

            key = Storage.instance().entities().get('iobroker', entity)

            if key:
                for entity_type in key:
                    if entity_type == 'switch':

                        if 'val' not in data:
                            return

                        if not bool(data['val']):
                            Storage.instance().entities().changeState(
                                'iobroker',
                                entity,
                                'switch',
                                {
                                    'entity_id': entity,
                                    'state': 'off'
                                })
                        else:
                            Storage.instance().entities().changeState(
                                'iobroker',
                                entity,
                                'switch',
                                {
                                    'entity_id': entity,
                                    'state': 'on'
                                })
                    elif entity_type == 'sensor':
                        if 'val' not in data:
                            return

                        unit = ''

                        if 'common' in self.entities[entity] and 'unit' in self.entities[entity]['common']:
                            unit = self.entities[entity]['common']['unit']

                        Storage.instance().entities().changeState(
                            'iobroker',
                            entity,
                            'sensor',
                            {
                                'entity_id': entity,
                                'state': data['val'],
                                'unit': unit
                            })
                    elif entity_type == 'weather':
                        if not key['weather']:
                            key['weather'] = {
                                'entity_id': '',
                                'condition': '',
                                'condition_label': '',
                                'condition_icon': '',
                                'temperature': '',
                                'humidity': '',
                                'pressure': '',
                                'wind_direction': '',
                                'wind_speed': '',
                                'forecast': [{
                                    'condition': '',
                                    'condition_icon': '',
                                    'day': '',
                                    'temperature': ''
                                }, {
                                    'condition': '',
                                    'condition_icon': '',
                                    'day': '',
                                    'temperature': ''
                                }, {
                                    'condition': '',
                                    'condition_icon': '',
                                    'day': '',
                                    'temperature': ''
                                }, {
                                    'condition': '',
                                    'condition_icon': '',
                                    'day': '',
                                    'temperature': ''
                                }, {
                                    'condition': '',
                                    'condition_icon': '',
                                    'day': '',
                                    'temperature': ''
                                }]
                            }

                        key['weather']['entity_id'] = entity
                        parts = original_entity.split('.')

                        if parts[3] == 'current':
                            if parts[4] == 'temperature':
                                key['weather']['temperature'] = round(data['val'], 1)
                            elif parts[4] == 'humidity':
                                key['weather']['humidity'] = data['val']
                            elif parts[4] == 'pressure':
                                key['weather']['pressure'] = data['val']
                            elif parts[4] == 'windSpeed':
                                key['weather']['wind_speed'] = round(data['val'] * 3.6, 1)
                            elif parts[4] == 'windDirection':
                                key['weather']['wind_direction'] = self.wind_bearing_to_text(data['val'])
                            elif parts[4] == 'icon':
                                key['weather']['condition_icon'] = self.weather_icons[data['val']]
                            elif parts[4] == 'state':
                                key['weather']['condition_label'] = data['val']
                        if parts[3] in ['day1', 'day2', 'day3', 'day4', 'day5']:
                            days = ['day1', 'day2', 'day3', 'day4', 'day5']

                            if parts[4] == 'temperatureMax':
                                key['weather']['forecast'][days.index(parts[3])]['temperature'] = round(data['val'], 1)
                            elif parts[4] == 'icon':
                                key['weather']['forecast'][days.index(parts[3])]['condition_icon'] = self.weather_icons[data['val']]
                            elif parts[4] == 'date':
                                key['weather']['forecast'][days.index(parts[3])]['day'] = self.weekdays[datetime.fromtimestamp(data['val'] / 1000).weekday()]

                        Storage.instance().entities().changeState(
                            'iobroker',
                            entity,
                            'weather',
                            key['weather']
                        )
                    else:
                        print(entity_type + ' for ' + entity + ' is currently not supported for ioBroker. Currently only sensor and switch are supported.')


    def init_objects(self, err, data):
        for i in data:
            self.entities[i] = data[i]

        self.emit('getStates', callback=self.init_states)

    def init_states(self, err, data):
        for i in data:
            self.on_state_change(i, data[i])

    @Slot()
    def setState(self, entity_id, entity_type, value):
        if entity_type == 'switch' or entity_type == 'light':
            if value == 'on':
                self.emit('setState', data=(entity_id, {'val': True, 'ack': False}))
            else:
                self.emit('setState', data=(entity_id, {'val': False, 'ack': False}))
