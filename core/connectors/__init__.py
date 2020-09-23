from PySide2.QtCore import QObject, Slot

from core.connectors.homeassistant import HomeAssistant
from core.connectors.iobroker import IoBroker
from core.storage import Storage

class Connectors(QObject):
    _instance = None

    def __init__(self):
        QObject.__init__(self)
        self._instance = None
        self.started = False

    def __new__(cls):
        if cls._instance is None:
            self = cls._instance = super(Connectors, cls).__new__(cls)
            self._connectors = {}
            self.load_connectors()



        return cls._instance

    def load_connectors(self):
        config = Storage.instance().config()

        if config.get('connectors.iobroker'):
            self.set('iobroker', IoBroker(config.get('connectors.iobroker')))
        if config.get('connectors.homeassistant'):
            self.set('homeassistant', HomeAssistant(config.get('connectors.homeassistant')))

    @Slot()
    def start(self):
        if not self.started:
            for connector in self._connectors:
                self._connectors[connector].start()
            self.started = True

    @staticmethod
    def instance():
        return Connectors._instance

    @Slot(str, "QVariant")
    def set(self, key, connector):
        self._connectors[key] = connector

    @Slot(str, result="QVariant")
    def get(self, key):
        return self._connectors[key]
