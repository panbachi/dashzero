import os
import subprocess

from core.platform.raspberry import Raspberry


class Shpi(Raspberry):
    def __init__(self, app, config):
        super(Shpi, self).__init__(app, config)

        if 'backlight' not in self.config:
            self.config['backlight'] = './backlight'

    def turn_display_on(self):
        if os.path.exists(self.config['backlight']):
            subprocess.call([self.config['backlight'], '31'])

    def turn_display_off(self):
        if os.path.exists(self.config['backlight']):
            subprocess.call([self.config['backlight'], '0'])
