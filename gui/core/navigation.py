from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from gui.core.room import Room


class NavigationItem(BoxLayout, MDTabsBase):
    def __init__(self, config, **kwargs):
        super(NavigationItem, self).__init__(**kwargs)

        self.text = config['icon']
        self.tab_label.font_size = "48sp"
        self.anim_duration = 0.0

        self.room = Room(config)
        self.add_widget(self.room)


class Navigation(MDTabs):
    def __init__(self, config, **kwargs):
        super(Navigation, self).__init__(**kwargs)

        self.tab_bar_height = "80dp"
        self.tab_indicator_height = "6dp"

        self.rooms = config

        for room in self.rooms:
            self.add_widget(NavigationItem(room))
