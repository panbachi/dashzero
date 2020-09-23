import os
from core.connectors.shpi import SHPI as Connector
from core.storage import Storage


class SHPI:
    def __init__(self, config):
        self.config = config

        self.connector = Connector(config)
        Storage.instance().connectors().set('shpi', self.connector)
        self.connector.read_initial_states()

    def sleep(self):
        os.system('i2cset -y 2 0x2A 0x87 0')

    def wakeup(self):
        os.system('i2cset -y 2 0x2A 0x87 31')
