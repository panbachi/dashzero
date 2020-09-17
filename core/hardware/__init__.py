from PySide2.QtCore import QObject, Slot
from core.hardware.shpi import SHPI
from core.hardware.raspberry import Raspberry
from core.hardware.undefined import Undefined
from core.connectors.shpi import SHPI as Connector
from core.storage import Storage


class Hardware(QObject):
    def __init__(self, config):
        QObject.__init__(self)
        self.hardware = None

        try:
            if config['hardware']['type'] == 'shpi':
                self.hardware = SHPI(config['hardware'])
                self.connector = Connector(config['hardware'])
                Storage.instance().connectors().set('shpi', self.connector)
                self.connector.read_initial_states()
            elif config['hardware']['type'] == 'raspberry':
                self.hardware = Raspberry(config['hardware'])
        except Exception:
            print('Unknown hardware. Configure your hardware in config.yaml')
            self.hardware = Undefined({})

    @Slot()
    def sleep(self):
        if self.hardware:
            self.hardware.sleep()

    @Slot()
    def wakeup(self):
        if self.hardware:
            self.hardware.wakeup()
