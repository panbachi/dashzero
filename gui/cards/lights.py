# -*- coding: utf-8 -*-
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDIcon
from kivymd.uix.list import MDList, OneLineIconListItem, ILeftBody
from kivy.app import App
from kivy.utils import get_color_from_hex


class LightsIcon(ILeftBody, MDIcon):
    def __init__(self, **kwargs):
        super(LightsIcon, self).__init__(**kwargs)

        '''
        configure MDIcon properties
        '''
        self.theme_text_color =	'Custom'
        self.text_color = get_color_from_hex('#F1C40F')
        self.font_size = '48dp'


class LightsItem(OneLineIconListItem):
    def __init__(self, config, **kwargs):
        super(LightsItem, self).__init__(**kwargs)

        self.ids._lbl_primary.font_style = 'H4'
        self.ids._lbl_primary.valign = 'center'
        self._txt_bot_pad = '30dp'
        self.height = '100dp'

        '''
        register event listener
        '''
        App.get_running_app().bind(on_state_changed=self.on_state_changed)

        '''
        configure OneLineIconListItem properties
        '''
        self.text = config['name']

        '''
        configure LightsItem properties
        '''
        self.config = config
        self.activated = False

        '''
        configure icon
        '''
        self.icon = LightsIcon(icon=self.config['icon'])

        '''
        add widgets
        '''
        self.add_widget(self.icon)

    def on_state_changed(self, obj, value):
        if value['entity_id'] == self.config['entity_id']:
            if value['state'] == 'on':
                self.activate()
            else:
                self.deactivate()

    def change_state(self):
        if self.activated:
            state = 'off'
        else:
            state = 'on'

        App.get_running_app().change_state('homeassistant', entity_id=self.config['entity_id'], state=state)

    def on_press(self):
        self.change_state()

    def on_release(self):
        if self.activated:
            self.icon.text_color = get_color_from_hex('#F1C40F')
        else:
            self.icon.text_color = get_color_from_hex('#BDC3C7')

    def activate(self):
        self.activated = True
        self.icon.text_color = get_color_from_hex('#F1C40F')

    def deactivate(self):
        self.activated = False
        self.icon.text_color = get_color_from_hex('#BDC3C7')


class Lights(ScrollView):
    def __init__(self, config, **kwargs):
        super(Lights, self).__init__(**kwargs)

        '''
        configure list
        '''
        self.list = MDList()

        for entity in config['entities']:
            item = LightsItem(config=entity)
            self.list.add_widget(item)

        '''
        add widgets
        '''
        self.add_widget(self.list)
