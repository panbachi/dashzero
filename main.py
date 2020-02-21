import os
import yaml

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp

from gui.core import Navigation

from core.connectors import HomeAssistant
from core.platform import Shpi

if os.path.exists('config.yaml'):
    config_file = 'config.yaml'
else:
    config_file = 'config.example.yaml'

with open(config_file, 'r') as stream:
    config = yaml.safe_load(stream)


class MainScreen(FloatLayout):
    def __init__(self, config, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

        self.navigation = Navigation(config['rooms'])

        self.size = Window.size

        self.backlight_trigger = Clock.schedule_once(self.turn_display_off, 5)
        self.backlight = True

        self.add_widget(self.navigation)

    def on_touch_down(self, touch):
        if not self.backlight:
            print(touch)
            self.turn_display_on()
            print(self.backlight)

        Clock.unschedule(self.backlight_trigger)
        self.backlight_trigger = Clock.schedule_once(self.turn_display_off, 5)

        return super().on_touch_down(touch)

    def turn_display_off(self, dt):
        print('display is off')
        self.backlight = False

        if self.app.platform:
            self.app.platform.turn_display_off()

    def turn_display_on(self):
        print('display is on')
        self.backlight = True

        if self.app.platform:
            self.app.platform.turn_display_on()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.register_event_type('on_state_changed')
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Gray"
        super().__init__(**kwargs)
        self.config = config
        self.connectors = {}
        self.platform = None

        if 'homeassistant' in config:
            self.connectors['homeassistant'] = HomeAssistant(self, self.config['homeassistant'])

        if 'shpi' in config:
            self.platform = Shpi(self, self.config['shpi'])

    def build(self):
        self.root = MainScreen(config)
        Window.size = (800, 480)

        for connector in self.connectors:
            self.connectors[connector].connect_to_server()

        return self.root

    def change_state(self, connector, entity_id, state):
        if connector in self.connectors:
            self.connectors[connector].change_state(entity_id, state)

    def change_temperature(self, connector, entity_id, temperature):
        if connector in self.connectors:
            self.connectors[connector].change_temperature(entity_id, temperature)

    def on_state_changed(self, *args, **kwargs):
        pass


if __name__ == "__main__":
    MainApp().run()
