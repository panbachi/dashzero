# -*- coding: utf-8 -*-
from ics import Calendar
import requests
import arrow
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDIcon
from kivymd.uix.list import MDList, OneLineIconListItem, ILeftBody


class GarbageIcon(ILeftBody, MDIcon):
    def __init__(self, **kwargs):
        super(GarbageIcon, self).__init__(**kwargs)

        '''
        configure GarbageIcon properties
        '''
        self.theme_text_color = 'Custom'
        self.font_size = '48dp'


class GarbageItem(OneLineIconListItem):
    def __init__(self, color, **kwargs):
        super(GarbageItem, self).__init__(**kwargs)

        self.ids._lbl_primary.font_style = 'H4'
        self.ids._lbl_primary.valign = 'center'
        self._txt_bot_pad = '30dp'
        self.height = '100dp'

        '''
        configure icon
        '''
        self.icon = GarbageIcon(icon='delete-empty')

        if color == 'blue':
            self.icon.text_color = [0x29 / 255.0, 0x80 / 255.0, 0xB9 / 255.0, 1]
        elif color == 'yellow':
            self.icon.text_color = [0xF1 / 255.0, 0xC4 / 255.0, 0x0F / 255.0, 1]
        elif color == 'grey':
            self.icon.text_color = [0x7F / 255.0, 0x8C / 255.0, 0x8D / 255.0, 1]
        elif color == 'brown':
            self.icon.text_color = [0x79 / 255.0, 0x55 / 255.0, 0x48 / 255.0, 1]

        '''
        add widgets
        '''
        self.add_widget(self.icon)


class Garbage(ScrollView):
    def __init__(self, config, **kwargs):
        super(Garbage, self).__init__(**kwargs)

        '''
        configure Garbage properties
        '''
        self.config = config

        self.blue = ''
        self.yellow = ''
        self.grey = ''
        self.brown = ''

        '''
        collect data
        '''
        self.fetch_calendar()

        '''
        configure list
        '''
        self.list = MDList()

        if 'blue' in self.config['filter']:
            self.blue_item = GarbageItem(text=self.blue, color='blue')
            self.list.add_widget(self.blue_item)

        if 'yellow' in self.config['filter']:
            self.yellow_item = GarbageItem(text=self.yellow, color='yellow')
            self.list.add_widget(self.yellow_item)

        if 'grey' in self.config['filter']:
            self.grey_item = GarbageItem(text=self.grey, color='grey')
            self.list.add_widget(self.grey_item)

        if 'brown' in self.config['filter']:
            self.brown_item = GarbageItem(text=self.brown, color='brown')
            self.list.add_widget(self.brown_item)

        '''
        add widgets
        '''
        self.add_widget(self.list)

    def fetch_calendar(self):
        url = self.config['url']
        c = Calendar(requests.get(url).text)

        for event in list(c.timeline.start_after(arrow.now().floor('day'))):
            date = event.begin.format('DD.MM.YYYY') + ' (' + event.begin.humanize(arrow.utcnow(), locale='de', granularity='day') + ')'
            if 'blue' in self.config['filter'] \
                    and self.config['filter']['blue'] in event.name \
                    and not self.blue:
                self.blue = date
            elif 'grey' in self.config['filter'] \
                    and self.config['filter']['grey'] in event.name \
                    and not self.grey:
                self.grey = date
            elif 'yellow' in self.config['filter'] \
                    and self.config['filter']['yellow'] in event.name \
                    and not self.yellow:
                self.brown = date
            elif 'brown' in self.config['filter'] \
                    and self.config['filter']['brown'] in event.name \
                    and not self.brown:
                self.yellow = date
