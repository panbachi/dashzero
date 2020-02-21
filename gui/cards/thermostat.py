# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.list import MDList, TwoLineIconListItem, ILeftBody
from kivy.graphics import Color
from kivy.graphics import Rectangle


class ThermostatTempButton(ButtonBehavior, MDIcon):
    def __init__(self, kind, **kwargs):
        super(ThermostatTempButton, self).__init__(**kwargs)

        '''
        configure MDIcon properties
        '''
        self.size_hint = (None, None)
        self.size = (350, 100)
        self.theme_text_color = 'Custom'
        self.markup = True
        self.font_size = '100px'
        self.halign = 'center'

        '''
        configure ThermostatTempButton properties
        '''
        self.kind = kind

        if self.kind == 'plus':
            self.text_color = get_color_from_hex('#E74C3C')
            self.icon = 'plus'
        else:
            self.text_color = get_color_from_hex('#3498DB')
            self.icon = 'minus'

    def on_press(self):
        if self.kind == 'plus':
            self.text_color = get_color_from_hex('#C0392B')
            self.parent.increase_temp()
        else:
            self.text_color = get_color_from_hex('#2980B9')
            self.parent.decrease_temp()

    def on_release(self):
        if self.kind == 'plus':
            self.text_color = get_color_from_hex('#E74C3C')
        else:
            self.text_color = get_color_from_hex('#3498DB')


class ThermostatSensorIcon(ILeftBody, MDIcon):
    pass


class ThermostatSensor(TwoLineIconListItem):
    def __init__(self, config, **kwargs):
        super(ThermostatSensor, self).__init__(**kwargs)

        '''
        register event listener
        '''
        App.get_running_app().bind(on_state_changed=self.on_state_changed)

        '''
        configure BoxLayout properties
        '''
        self.orientation = 'vertical'

        '''
        configure ThermostatSensor properties
        '''
        self.config = config

        self.icon = ThermostatSensorIcon(icon=self.config['icon'])
        self.text = self.config['name']
        self.secondary_text = ''

        '''
        add widgets
        '''
        self.add_widget(self.icon)

    def on_state_changed(self, obj, value):
        if value['entity_id'] == self.config['entity_id']:
            uom = value['attributes']['unit_of_measurement']
            self.secondary_text = value['state'] + uom


class ThermostatControl(ButtonBehavior, MDIcon):
    def __init__(self, config, **kwargs):
        super(ThermostatControl, self).__init__(**kwargs)

        '''
        configure Label properties
        '''
        self.markup = True
        self.font_size = '50px'
        self.halign = 'center'
        self.valign = 'middle'
        # self.size_hint = (None, None)
        self.text_size = self.size

        '''
        configure ThermostatControl properties
        '''
        self.config = config
        self.kind = self.config['type']
        self.icon = self.config['icon']
        self.color = get_color_from_hex(self.config['color'])

    def on_press(self):
        self.parent.parent.set_temp(self.config['value'])


class Thermostat(FloatLayout):
    def __init__(self, config, **kwargs):
        super(Thermostat, self).__init__(**kwargs)

        self.app = App.get_running_app()

        '''
        register event listener
        '''
        self.app.bind(on_state_changed=self.on_state_changed)

        '''
        configure Thermostat properties
        '''
        self.config = config
        self.current_set = 0

        '''
        configure temp plus button
        '''
        self.temp_plus = ThermostatTempButton(
            pos=(0, 220),
            kind='plus'
        )

        '''
        configure temp minus button
        '''
        self.temp_minus = ThermostatTempButton(
            pos=(0, 0),
            kind='minus'
        )

        '''
        configure temp value
        '''
        self.temp_value = MDLabel(
            size=(350, 120),
            pos=(0, 100),
            font_style='H1',
            size_hint=(None, None),
            valign='middle',
            halign='center',
            font_size='100px',
            markup=True,
            text=''
        )

        '''
        configure sensors
        '''
        self.sensors = ScrollView(
            size_hint=(None, None),
            size=(440, 220),
            pos=(360, 105)
        )

        self.sensors_list = MDList()

        for sensor in config['sensors']:
            self.sensors_list.add_widget(ThermostatSensor(config=sensor))

        self.sensors.add_widget(self.sensors_list)

        '''
        configure controls
        '''
        self.controls = BoxLayout(
            pos=(360, 0),
            size_hint=(None, None),
            size=(440, 100)
        )

        for control in config['controls']:
            self.controls.add_widget(ThermostatControl(config=control))

        '''
        add widgets
        '''
        self.add_widget(self.temp_plus)
        self.add_widget(self.temp_value)
        self.add_widget(self.temp_minus)
        self.add_widget(self.sensors)
        self.add_widget(self.controls)

    def on_state_changed(self, obj, value):
        if value['entity_id'] == self.config['entity_id']:
            uom = '[sup]' + self.config['unit_of_measurement'] + '[/sup]'
            self.current_set = value['attributes']['temperature']
            self.temp_value.text = str(self.current_set) + uom

    def increase_temp(self):
        temperature = self.current_set + 1

        if temperature > 30:
            temperature = 30

        self.set_temp(temperature)

    def decrease_temp(self):
        temperature = self.current_set - 1

        if temperature < 4:
            temperature = 4

        self.set_temp(temperature)

    def set_temp(self, temperature):
        self.app.change_temperature('homeassistant', entity_id=self.config['entity_id'], temperature=temperature)
