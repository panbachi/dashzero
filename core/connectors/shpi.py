import os
from core.storage import Storage
from PySide2.QtCore import QObject, Slot, QTimer


class SHPI(QObject):
    def __init__(self, config):
        QObject.__init__(self)
        self.config = config
        self.__update_timer = QTimer(self)
        self.__update_timer.setInterval(2000)
        self.__update_timer.timeout.connect(self.read_initial_states)
        self.__update_timer.start()

    def read_initial_states(self):
        fan = os.popen('i2cget -y 2 0x2A 0x13').read().strip()
        if int(fan, 16) == 0:
            Storage.instance().entities().changeState('shpi', {'entity_id': 'fan.main', 'state': 'on'})
        else:
            Storage.instance().entities().changeState('shpi', {'entity_id': 'fan.main', 'state': 'off'})

        relay_1 = os.popen('i2cget -y 2 0x2A 0x0D').read().strip()
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_1',
                                                           'state': 'on' if int(relay_1, 16) == 0 else 'off'})

        relay_2 = os.popen('i2cget -y 2 0x2A 0x0E').read().strip()
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_2',
                                                           'state': 'on' if int(relay_2, 16) == 0 else 'off'})

        relay_3 = os.popen('i2cget -y 2 0x2A 0x0F').read().strip()
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_3',
                                                           'state': 'on' if int(relay_3, 16) == 0 else 'off'})

        airquality = os.popen('i2cget -y 2 0x2A 0x04').read().strip()
        airquality = int(airquality, 16) / 1024 * 100
        Storage.instance().entities().changeState('shpi', {'entity_id': 'sensor.airquality',
                                                           'state': round(airquality, 1),
                                                           'unit': '%'})

        temperature = os.popen('i2cget -y 2 0x2A 0x04').read().strip()
        temperature = int(temperature, 16) / 1024 * 100
        Storage.instance().entities().changeState('shpi', {'entity_id': 'sensor.temperature',
                                                           'state': round(temperature, 1),
                                                           'unit': '°C'})
        current = os.popen('i2cget -y 2 0x2A 0x04').read().strip()
        Storage.instance().entities().changeState('shpi', {'entity_id': 'sensor.current',
                                                           'state': int(current, 16),
                                                           'unit': 'A'})

    def turn_on_fan(self):
        os.system('i2cset -y 2 0x2A 0x93 0')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'fan.main', 'state': 'on'})

    def turn_off_fan(self):
        os.system('i2cset -y 2 0x2A 0x93 254')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'fan.main', 'state': 'off'})

    def turn_on_relay_1(self):
        os.system('i2cset -y 2 0x2A 0x8D 0x00')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_1', 'state': 'on'})

    def turn_off_relay_1(self):
        os.system('i2cset -y 2 0x2A 0x8D 0xFF')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_1', 'state': 'off'})

    def turn_on_relay_2(self):
        os.system('i2cset -y 2 0x2A 0x8E 0x00')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_2', 'state': 'on'})

    def turn_off_relay_2(self):
        os.system('i2cset -y 2 0x2A 0x8E 0xFF')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_2', 'state': 'off'})

    def turn_on_relay_3(self):
        os.system('i2cset -y 2 0x2A 0x8F 0x00')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_3', 'state': 'on'})

    def turn_off_relay_3(self):
        os.system('i2cset -y 2 0x2A 0x8F 0xFF')
        Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_3', 'state': 'off'})

    @Slot(str, "QVariant")
    def setState(self, entityId, state):
        if entityId == 'fan.main':
            if state == 'on':
                self.turn_on_fan()
            else:
                self.turn_off_fan()

        if entityId == 'switch.relay_1':
            if state == 'on':
                self.turn_on_relay_1()
            else:
                self.turn_off_relay_1()

        if entityId == 'switch.relay_2':
            if state == 'on':
                self.turn_on_relay_2()
            else:
                self.turn_off_relay_2()

        if entityId == 'switch.relay_3':
            if state == 'on':
                self.turn_on_relay_3()
            else:
                self.turn_off_relay_3()
