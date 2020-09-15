from PySide2.QtCore import QObject, Slot


class Config(QObject):
    _instance = None

    def __init__(self, config=None):
        QObject.__init__(self)
        self._instance = None

    def __new__(cls, config=None):
        if cls._instance is None:
            self = cls._instance = super(Config, cls).__new__(cls)
            self.config = config
            self.connectors = {}

        return cls._instance

    @staticmethod
    def instance():
        return Config._instance

    @Slot(str, result="QVariant")
    def get(self, key):
        if not key:
            return self.config

        keys = key.split('.')
        value = None

        for i in keys:
            if not value:
                value = self.config

            if i in value:
                value = value[i]
            else:
                return None

        return value

    @Slot(str, "QVariant")
    def setConnector(self, key, connector):
        if not self.connectors:
            self.connectors = {}

        self.connectors[key] = connector

    @Slot(str, "QVariant")
    def set(self, key, value):
        self.config[key] = value

    @Slot(str)
    def getConnector(self, key):
        return self.connectors[key]
