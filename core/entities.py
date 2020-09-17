from PySide2.QtCore import QObject, Slot, Signal
from core.storage import Storage


class Entities(QObject):
    _instance = None

    def __init__(self):
        QObject.__init__(self)

    def __new__(cls):
        if cls._instance is None:
            self = cls._instance = super(Entities, cls).__new__(cls)
            self.entities = {}
        return cls._instance

    def get(self, connector, key):
        if connector not in self.entities:
            self.entities[connector] = {}

        if key not in self.entities[connector]:
            self.entities[connector][key] = {}

        return self.entities[connector][key]

    def set(self, connector, key, value):
        if connector not in self.entities:
            self.entities[connector] = {}

        if key not in self.entities[connector]:
            self.entities[connector][key] = value

        self.changedSignal.emit(connector, key, value)

    changedSignal = Signal(str, str, "QVariant")

    @Slot(str, str, str)
    def setState(self, connector, key, value):
        try:
            Storage.instance().connectors().get(connector).setState(key, value)
        except Exception:
            pass

    @Slot(str, "QJsonObject")
    @Slot(str, "QVariant")
    def changeState(self, connector, new_state):
        self.set(connector, new_state['entity_id'], new_state)

    @Slot()
    def initialize(self):
        for c in self.entities:
            for k in self.entities[c]:
                self.changedSignal.emit(c, k, self.entities[c][k])
