from PySide2.QtCore import QObject, Slot


class Connectors(QObject):
    _instance = None

    def __init__(self):
        QObject.__init__(self)
        self._instance = None

    def __new__(cls):
        if cls._instance is None:
            self = cls._instance = super(Connectors, cls).__new__(cls)
            self._connectors = {}

        return cls._instance

    @staticmethod
    def instance():
        return Connectors._instance

    @Slot(str, "QVariant")
    def set(self, key, connector):
        self._connectors[key] = connector

    @Slot(str, result="QVariant")
    def get(self, key):
        return self._connectors[key]
