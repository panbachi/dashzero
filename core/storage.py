from PySide2.QtCore import QObject, Slot


class Storage(QObject):
    _instance = None

    def __init__(self):
        QObject.__init__(self)
        self._instance = None

    def __new__(cls):
        if cls._instance is None:
            self = cls._instance = super(Storage, cls).__new__(cls)
            self._config = None
            self._connectors = None
            self._entities = None
            self._hardware = None

        return cls._instance

    @staticmethod
    def instance():
        if Storage._instance is None:
            return Storage()
        return Storage._instance

    def setConnectors(self, connectors):
        self._connectors = connectors

    @Slot(result="QVariant")
    def connectors(self):
        return self._connectors

    def setConfig(self, config):
        self._config = config

    @Slot(result="QVariant")
    def config(self):
        return self._config

    def setEntities(self, entities):
        self._entities = entities

    @Slot(result="QVariant")
    def entities(self):
        return self._entities

    def setHardware(self, hardware):
        self._hardware = hardware

    @Slot(result="QVariant")
    def hardware(self):
        return self._hardware
