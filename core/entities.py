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

    @Slot(str, str, str)
    @Slot(str, str)
    def get(self, connector, entity_id, entity_type=None):

        if connector not in self.entities:
            return None

        if entity_id not in self.entities[connector]:
            return None

        if entity_type is not None:
            if entity_type not in self.entities[connector][entity_id]:
                return None

            return self.entities[connector][entity_id][entity_type]

        return self.entities[connector][entity_id]

    def set(self, connector, entity_id, entity_type, value):
        if connector not in self.entities:
            self.entities[connector] = {}

        if entity_id not in self.entities[connector]:
            self.entities[connector][entity_id] = {}

        self.entities[connector][entity_id][entity_type] = value

        self.changedSignal.emit(connector, entity_id, entity_type, value)

    def find_entity_by_key_without_prefix(self, connector, key):
        if connector not in self.entities:
            return False

        for entity in self.entities[connector]:
            keys = entity.split('.')
            keys.pop(0)
            entity = '.'.join(keys)

            if key == entity:
                return key

        return None

    changedSignal = Signal(str, str, str, "QVariant")

    @Slot(str, str, str, "QJsonObject")
    @Slot(str, str, str, "QVariant")
    @Slot(str, str, str, str)
    def setState(self, connector, entity_id, entity_type, value):
        try:
            Storage.instance().connectors().get(connector).setState(entity_id, entity_type, value)
        except Exception as e:
            print('EXCEPTION', e)
            pass

    @Slot(str, str, str, "QJsonObject")
    @Slot(str, str, str, "QVariant")
    def changeState(self, connector, entity_id, entity_type, new_state):
        self.set(connector, entity_id, entity_type, new_state)

    @Slot()
    def initialize(self):
        for c in self.entities:
            for k in self.entities[c]:
                for t in self.entities[c][k]:
                    self.changedSignal.emit(c, k, t, self.entities[c][k][t])

    @Slot(str, str, str)
    def registerEntity(self, connector, entity_id, entity_type):
        if connector not in self.entities:
            self.entities[connector] = {}

        if entity_id not in self.entities[connector]:
            self.entities[connector][entity_id] = {}

        self.entities[connector][entity_id][entity_type] = {}