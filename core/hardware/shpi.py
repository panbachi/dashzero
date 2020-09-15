import os


class SHPI:
    def __init__(self, config):
        self.config = config

    def sleep(self):
        os.system('i2cset -y 2 0x2A 0x87 0')

    def wakeup(self):
        os.system('i2cset -y 2 0x2A 0x87 31')
