from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.screenmanager import FadeTransition
from gui.cards import Door, Garbage, Lights, Thermostat, Weather


class RoomNavigation(MDBottomNavigation):
    def __init__(self, config, **kwargs):
        super(RoomNavigation, self).__init__(**kwargs)
        self.height = '80dp'
        self.ids.bottom_panel.height = '80dp'
        self.ids.tab_bar.height = '80dp'
        self.ids.tab_manager.transition.duration = 0.0

        for card in config:
            icon = None
            content = None

            if card['type'] == 'lights':
                icon = 'lightbulb'
                content = Lights(card)
            elif card['type'] == 'thermostat':
                icon = 'thermometer'
                content = Thermostat(card)
            elif card['type'] == 'garbage':
                icon = 'delete-empty'
                content = Garbage(card)
            elif card['type'] == 'weather':
                icon = 'weather-partly-cloudy'
                content = Weather(card)
            elif card['type'] == 'door':
                icon = 'door'
                content = Door(card)

            if content:
                item = MDBottomNavigationItem(name=card['name'], text=card['name'], icon=icon)
                item.add_widget(content)
                self.add_widget(item)

        for i in self.ids.tab_bar.children:
            i.ids._label_icon.font_size = '48sp'


class Room(FloatLayout):
    def __init__(self, config, **kwargs):
        super(Room, self).__init__(**kwargs)
        self.config = config

        self.content = MDLabel(text=self.config['name'], halign="center", theme_text_color="Primary", font_style="H6")
        self.navigation = RoomNavigation(config['cards'])

        self.add_widget(self.content)
        self.add_widget(self.navigation)
