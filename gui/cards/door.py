# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDIcon
from kivy.app import App


class DoorOpener(ButtonBehavior, MDIcon):
    def __init__(self, config, **kwargs):
        super(DoorOpener, self).__init__(**kwargs)

        '''
        register event listener
        '''
        App.get_running_app().bind(on_state_changed=self.on_state_changed)

        '''
        configure MDIcon properties
        '''
        self.theme_text_color = 'Custom'
        self.font_size = '100px'
        self.halign = 'center'
        self.size_hint = (0.4, 1)

        '''
        configure DoorOpener properties
        '''
        self.config = config
        self.opened = False

    def open(self):
        self.opened = True
        self.icon = 'door-open'
        self.text_color = [0x27 / 255.0, 0xAE / 255.0, 0x60 / 255.0, 1]

    def close(self):
        self.opened = False
        self.icon = 'door-closed'
        self.text_color = [0xC0 / 255.0, 0x39 / 255.0, 0x2B / 255.0, 1]

    def on_state_changed(self, obj, value):
        if value['entity_id'] == self.config['entity_id']:
            if value['state'] == 'on':
                self.open()
            else:
                self.close()

    def on_press(self):
        if self.opened:
            state = 'off'
        else:
            state = 'on'

        App.get_running_app().change_state('homeassistant', entity_id=self.config['entity_id'], state=state)


class DoorCamera(AsyncImage):
    def __init__(self, config, **kwargs):
        super(DoorCamera, self).__init__(**kwargs)

        '''
        register event listener
        '''
        App.get_running_app().bind(on_state_changed=self.on_state_changed)

        '''
        configure DoorCamera properties
        '''
        self.config = config

    def on_state_changed(self, obj, value):
        if value['entity_id'] == self.config['entity_id']:
            self.source = value['attributes']['entity_picture']
            self.reload()


class Door(BoxLayout):
    def __init__(self, config, **kwargs):
        super(Door, self).__init__(**kwargs)

        '''
        configure door camera
        '''
        self.camera = DoorCamera(config['camera'])

        '''
        configure door opener
        '''
        self.opener = DoorOpener(config['opener'])

        '''
        add widgets
        '''
        self.add_widget(self.camera)
        self.add_widget(self.opener)
