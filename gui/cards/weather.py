# -*- coding: utf-8 -*-
import arrow
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.utils import get_color_from_hex
from kivy.graphics import Color
from kivy.graphics import Rectangle


class WeatherForecastIcon(MDIcon):
    def __init__(self, font_size, **kwargs):
        super(WeatherForecastIcon, self).__init__(**kwargs)

        self.theme_text_color = 'Custom'
        self.text_color = get_color_from_hex('#3498DB')
        self.font_style = 'Icon'
        self.font_size = font_size
        self.halign = 'center'


class WeatherForecastItem(BoxLayout):
    def __init__(self, **kwargs):
        super(WeatherForecastItem, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.day = MDLabel(halign='center')
        self.icon = WeatherForecastIcon(font_size='35px')
        self.temperature = MDLabel(halign='center')

        self.add_widget(self.day)
        self.add_widget(self.icon)
        self.add_widget(self.temperature)


class WeatherForecast(BoxLayout):
    def __init__(self, **kwargs):
        super(WeatherForecast, self).__init__(**kwargs)

        self.size_hint = (None, None)
        self.pos = (0, 0)
        self.size = (800, 120)

        self.day_1 = WeatherForecastItem()
        self.day_2 = WeatherForecastItem()
        self.day_3 = WeatherForecastItem()
        self.day_4 = WeatherForecastItem()
        self.day_5 = WeatherForecastItem()

        self.add_widget(self.day_1)
        self.add_widget(self.day_2)
        self.add_widget(self.day_3)
        self.add_widget(self.day_4)
        self.add_widget(self.day_5)

    def populate(self, forecast):

        for num, data in enumerate(forecast, start=1):
            item = None

            if num == 1:
                item = self.day_1
            elif num == 2:
                item = self.day_2
            elif num == 3:
                item = self.day_3
            elif num == 4:
                item = self.day_4
            elif num == 5:
                item = self.day_5

            if item:
                item.day.text = arrow.get(data['datetime']).format('ddd', locale='de')
                item.icon.icon = self.parent.weather_icons[data['condition']]
                item.temperature.text = str(data['temperature']) + '°C'


class Weather(FloatLayout):
    def __init__(self, config, **kwargs):
        super(Weather, self).__init__(**kwargs)

        self.size_hint = (None, None)
        self.pos = (0, 0)
        self.size = (800, 320)

        self.config = config

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

        self.state = MDLabel(
            size_hint=(None, None),
            size=(800, 70),
            pos=(10, 250),
            font_style='H4',
            halign='center'
        )

        self.icon = WeatherForecastIcon(
            font_size='100px',
            size_hint=(None, None),
            size=(180, 130),
            pos=(0, 120)
        )

        self.temperature = MDLabel(
            size_hint=(None, None),
            size=(270, 130),
            pos=(180, 120),
            halign='center',
            font_style='H1',
            markup=True
        )

        self.humidity = MDLabel(
            size_hint=(None, None),
            size=(350, 40),
            pos=(450, 210),
            halign='left',
            valign='center'
        )
        self.humidity.text_size = self.humidity.size

        self.pressure = MDLabel(
            size_hint=(None, None),
            size=(350, 40),
            pos=(450, 165),
            halign='left',
            valign='center'
        )
        self.pressure.text_size = self.pressure.size

        self.wind = MDLabel(
            size_hint=(None, None),
            size=(350, 40),
            pos=(450, 120),
            halign='left',
            valign='center'
        )
        self.wind.text_size = self.wind.size

        self.forecast = WeatherForecast()

        self.add_widget(self.state)
        self.add_widget(self.icon)
        self.add_widget(self.temperature)
        self.add_widget(self.humidity)
        self.add_widget(self.pressure)
        self.add_widget(self.wind)
        self.add_widget(self.forecast)

        '''
        register event listener
        '''
        App.get_running_app().bind(on_state_changed=self.on_state_changed)

    def wind_bearing_to_text(self, degree):
        return self.cardinal_directions[int((int((int(degree) + 11.25) / 22.5) | 0) % 16)]

    def on_state_changed(self, obj, value):
        if value['entity_id'] == self.config['entity_id']:
            self.state.text = self.weather_labels[value['state']]
            self.icon.icon = self.weather_icons[value['state']]
            self.temperature.text = str(value['attributes']['temperature']) + '[sup]°C[/sup]'
            self.humidity.text = 'Luftfeuchtigkeit: ' + str(value['attributes']['humidity']) + ' %'
            self.pressure.text = 'Luftdruck: ' + str(value['attributes']['pressure']) + ' hPa'
            self.wind.text = 'Windgeschwindigkeit: ' + str(
                int(value['attributes']['wind_speed'])) + ' km/h (' + self.wind_bearing_to_text(
                value['attributes']['wind_bearing']) + ')'
            self.forecast.populate(value['attributes']['forecast'])
