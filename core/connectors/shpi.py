import sys
import os
import time
import ctypes
import fcntl
import struct
from core.storage import Storage
from PySide2.QtCore import QObject, Slot, QTimer

class I2C_MSG_S(ctypes.Structure):
    _fields_ = [("addr", ctypes.c_uint16),
                ("flags", ctypes.c_uint16),
                ("len", ctypes.c_uint16),
                ("buf", ctypes.c_char_p), ]


I2C_MSG_P = ctypes.POINTER(I2C_MSG_S)


class I2C_RDWR_S(ctypes.Structure):
    _fields_ = [("i2c_msg", I2C_MSG_P),
                ("nmsgs", ctypes.c_int), ]


I2C_TIMEOUT = 0x0702
I2C_RDWR = 0x0707
I2C_SMBUS = 0x0720
I2C_M_WR = 0x00
I2C_M_RD = 0x01


class I2C:
    def __init__(self, bus=None):
        # Initialize attributes
        self.device = ""
        self.name = ""
        self.addr = None
        self._dev = None
        if bus is not None:
            self.open(bus)

    def open(self, bus):
        self.device = "i2c-%s" % bus
        self._dev = open("/dev/%s" % self.device, 'rb')
        try:
            info = open("/sys/class/i2c-dev/%s/name" % self.device)
            self.name = info.readline().strip()
        except IOError as e:
            print(e)
            self.name = ""

    def close(self):
        if self._dev is not None:
            self._dev.close()
        self.device = ""
        self.name = ""
        self.addr = None
        self._dev = None

    """def get_funcs(self): #TODO neither I2C_FUNCS nor FUNCS are defined so this will fail
        if self._dev is None:
            raise IOError("Device not open")
        funcs = ctypes.c_ulong()
        _ret = fcntl.ioctl(self._dev.fileno(), I2C_FUNCS, funcs)
        return {key: True if funcs.value & val else False
                for key, val in FUNCS.iteritems()}"""

    def set_addr(self, addr):
        self.addr = int(addr)

    def set_timeout(self, timeout):
        if self._dev is None:
            raise IOError("Device not open")
        ret = fcntl.ioctl(self._dev.fileno(), I2C_TIMEOUT, timeout)
        return ret

    def crc8(self, crc, n):
        """ CRC checksum algorithm """
        data = crc ^ n
        for _i in range(0, 8):
            if ((data & 0x80) != 0x00):
                data = (data << 1) & 0xFF
                data ^= 0x07
            else:
                data = (data << 1) & 0xFF
        return data

    def read(self, nRead, addr=None):
        if self._dev is None:
            raise IOError("Device not open")
        if addr is None:
            addr = self.addr
        if addr is None:
            raise ValueError("No slave address specified!")
        if 0 > nRead > 65535:
            raise ValueError("Number of bytes must be 0 - 65535")
        read_msg = I2C_MSG_S(addr, I2C_M_RD, nRead, None)
        read_data = ctypes.create_string_buffer(nRead)
        read_msg.buf = ctypes.cast(read_data, ctypes.c_char_p)
        rdwr = I2C_RDWR_S(ctypes.pointer(read_msg), 1)
        ret = fcntl.ioctl(self._dev.fileno(), I2C_RDWR, rdwr)
        if ret != 1:
            raise IOError("Tried to send 1 message but %d sent" % ret, ret)
        return [ord(c) for c in read_data]

    def read_two_bytes(self, addr, addr_val, retries=0):  # utility function for brevity
        crc = 0
        try:
            crc = self.crc8(crc, addr_val)
            self.write([addr_val], addr)
            b = self.read(3, addr)
            crc = self.crc8(crc, b[0])
            crc = self.crc8(crc, b[1])
            time.sleep(0.001)
            if crc == b[2]:
                return b[0] | (b[1] << 8)
            else:
                raise Exception("crc 2 missmatch 0x{:02x}".format(addr_val))
        except Exception as e:  # potential inifinite loop - count repeats and break after n
            if retries < 10:
                time.sleep(0.1)
                return self.read_two_bytes(addr, addr_val, retries + 1)
            else:
                msg = "read_two_bytes error: {}".format(e)
                print(msg)

    def write(self, data, addr=None):
        if self._dev is None:
            raise IOError("Device not open")
        if addr is None:
            addr = self.addr
        if addr is None:
            raise ValueError("No slave address specified!")
        if len(data) > 5:
            raise ValueError("Cannot write more than 5 bytes at a time.")
        write_msg = I2C_MSG_S(addr, I2C_M_WR, len(data), None)
        if sys.version < '3':
            write_msg.buf = "".join(chr(x & 0xFF) for x in data)
        else:
            write_msg.buf = "".join(chr(x & 0xFF) for x in data).encode("L1")
        rdwr = I2C_RDWR_S(ctypes.pointer(write_msg), 1)
        ret = fcntl.ioctl(self._dev.fileno(), I2C_RDWR, rdwr)
        if ret != 1:
            raise IOError("Tried to send 1 message but %d sent" % ret, ret)
        return ret

    def rdwr(self, data, nRead, addr=None):
        if self._dev is None:
            raise IOError("Device not open")
        if addr is None:
            addr = self.addr
        if addr is None:
            raise ValueError("No slave address specified!")
        if len(data) > 16:
            raise ValueError("Write exceeds FIFO size!")
        if 0 > nRead > 32767:
            raise ValueError("Number of bytes must be 0 - 32767")
        write_msg = I2C_MSG_S(addr, I2C_M_WR, len(data), None)
        if sys.version < '3':
            write_msg.buf = "".join(chr(x & 0xFF) for x in data)
        else:
            write_msg.buf = "".join(chr(x & 0xFF) for x in data).encode("L1")
        nRead &= 0x7FFF
        read_msg = I2C_MSG_S(addr, I2C_M_RD, nRead, None)
        read_data = ctypes.create_string_buffer(nRead)
        read_msg.buf = ctypes.cast(read_data, ctypes.c_char_p)
        msgs = (I2C_MSG_S * 2)(write_msg, read_msg)
        rdwr = I2C_RDWR_S(msgs, 2)
        ret = fcntl.ioctl(self._dev.fileno(), I2C_RDWR, rdwr)
        if ret != 2:
            raise IOError("Tried to send 2 messages but %d sent" % ret, ret)
        return [ord(c) for c in read_data]

    def recover(self):
        try:
            addr = 3
            self.read(1, 0x2A)
            self.read(1, 0x2A)
            self.read(1, 0x2A)
            self.read(1, 0x2A)

            while ([0x00] == self.read(1, addr)):
                addr += 1
                if (addr > 119):
                    addr = 3
                # logging.debug(str(i) + '.', end = "")
            time.sleep(0.01)
        except:
            time.sleep(0.01)


class SHPI(QObject):
    ADDR_BH1750 = 0x23
    ADDR_32U4 = 0x2A
    ADDR_AHT10 = 0x38
    ADDR_SHT = 0x44
    ADDR_MLX = 0x5B
    ADDR_TOUCH = 0x5C
    ADDR_BMP = 0x77

    READ_A0 = 0x00
    READ_A1 = 0x01
    READ_A2 = 0x02
    READ_A3 = 0x03
    READ_A4 = 0x04
    READ_A5 = 0x05
    READ_A6 = 0x06
    READ_BACKLIGHT_LEVEL = 0x07
    READ_VENT_RPM = 0x08
    READ_ATMEGA_VOLT = 0x09
    READ_D13 = 0x10
    READ_HWB = 0x11
    READ_BUZZER = 0x12
    READ_VENT_PWM = 0x13
    READ_RELAY1CURRENT = 0x14
    READ_ATMEGA_TEMP = 0x0A
    READ_ATMEGA_RAM = 0x0B
    READ_RELAY1 = 0x0D
    READ_RELAY2 = 0x0E
    READ_RELAY3 = 0x0F

    WRITE_BACKLIGHT_LEVEL = 0x87
    WRITE_RELAY1 = 0x8D
    WRITE_RELAY2 = 0x8E
    WRITE_RELAY3 = 0x8F
    WRITE_D13 = 0x90
    WRITE_BUZZER = 0x92
    WRITE_VENT_PWM = 0x93
    WRITE_COLOR_RED = 0x94
    WRITE_COLOR_GREEN = 0x95
    WRITE_COLOR_BLUE = 0x96


    def __init__(self, config):
        QObject.__init__(self)
        self.config = config
        self.__update_timer = QTimer(self)
        self.__update_timer.setInterval(2000)
        self.__update_timer.timeout.connect(self.read_initial_states)
        self.__update_timer.start()
        self.bus = I2C(2)

        self.sht_temperature = 0
        self.bmp_temperature = 0

        self.dig_T = None
        self.dig_P = None
        self.init_aht()
        self.init_sht()
        self.init_bmp()
        self.init_mlx()
        self.init_bh()

        self.bus.recover()

    def init_aht(self):
        try:
            time.sleep(0.001)
            self.bus.write([0xA8, 0x00, 0x00], self.ADDR_AHT10)
            self.bus.write([0xAC, 0x00, 0x00], self.ADDR_AHT10)
            time.sleep(0.3)
            self.bus.write([0xE1, 0x08, 0x00], self.ADDR_AHT10)
            response = self.bus.read(1, self.ADDR_AHT10)
            if (response[0] & 0x68) == 0x08:
                print('Hint: AHT10 calibrated')
            else:
                print('Hint: AHT10 error occured')
        except:
            self.ADDR_AHT10 = 0
            print('Hint: no AHT10 found')

    def init_sht(self):
        try:
            time.sleep(0.001)
            self.bus.write([0x01], self.ADDR_SHT)
        except:
            self.ADDR_SHT = 0
            print('Hint: No SHT found')


    def init_bmp(self):
        try:
            time.sleep(0.001)
            b1 = bytes(self.bus.rdwr([0x88], 24, self.ADDR_BMP))
            self.dig_T = struct.unpack_from('<Hhh', b1, 0)
            self.dig_P = struct.unpack_from('<Hhhhhhhhh', b1, 6)
        except:
            print('Hint: No BMP280 found')
            self.ADDR_BMP = 0

    def init_bh(self):
        try:
            time.sleep(0.001)
            self.bus.write([0x01], self.ADDR_BH1750)  # power on BH1750
            time.sleep(0.05)
            data = self.bus.rdwr([0x23], 2, self.ADDR_BH1750)  # and check that did something!
            # TODO check data is valid else raise exception
        except:
            print('Hint: No BH1750')
            self.ADDR_BH1750 = 0

    def init_mlx(self):
        try:
            time.sleep(0.001)
            self.bus.rdwr([0x26], 2, self.ADDR_MLX)
        except:
            self.ADDR_MLX = False
            print('Hint: No MLX90615 found')

    def read_initial_states(self):
        self.get_current_time()
        self.get_cpu_temp()
        self.get_gpu_temp()
        self.get_sht_values()
        self.get_bmp_values()
        self.get_atmega_values()
        self.get_temperature()

    def get_current_time(self):
        current_time = time.strftime("%H:%M")

        Storage.instance().entities().changeState(
            'shpi', {
                'entity_id': 'sensor.current_time',
                'state': current_time,
                'unit': ''
            })

    def get_gpu_temp(self):
        gpu_temperature = round(float(os.popen("vcgencmd measure_temp").readline()[5:-3]), 1)

        Storage.instance().entities().changeState(
            'shpi', {
                'entity_id': 'sensor.gpu_temperature',
                'state': gpu_temperature,
                'unit': '°C'
            })

    def get_cpu_temp(self):
        cpu_temperature = round(float(os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()) / 1000, 1)

        Storage.instance().entities().changeState(
            'shpi', {
                'entity_id': 'sensor.cpu_temperature',
                'state': cpu_temperature,
                'unit': '°C'
            })

    def get_sht_values(self):
        if self.ADDR_SHT != 0:
            try:
                time.sleep(0.001)
                # clockstretching disabled , softreset: 0x30A2 or general call: 0x0006
                self.bus.write([0x24, 0x00], self.ADDR_SHT)
                time.sleep(0.05)
                data = self.bus.read(6, self.ADDR_SHT)
                sht_temperature = round(float(((data[0] * 256.0 + data[1]) * 175) / 65535.0 - 45), 1)
                sht_humidity = round(100 * (data[3] * 256 + data[4]) / 65535.0, 1)

                Storage.instance().entities().changeState(
                    'shpi', {
                        'entity_id': 'sensor.sht_temperature',
                        'state': sht_temperature,
                        'unit': '°C'
                    })

                self.sht_temperature = sht_temperature

                Storage.instance().entities().changeState(
                    'shpi', {
                        'entity_id': 'sensor.sht_humidity',
                        'state': sht_humidity,
                        'unit': '%'
                    })
            except Exception as e:
                print('error SHT: {}'.format(e))

    def get_bmp_values(self):
        if self.ADDR_BMP != 0:
            try:
                time.sleep(0.001)
                self.bus.write([0xF4, 0x27], self.ADDR_BMP)
                self.bus.write([0xF5, 0xA0], self.ADDR_BMP)
                data = self.bus.rdwr([0xF7], 8, self.ADDR_BMP)
                adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
                adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16
                _adc_h = data[6] * 256 + data[7]
                var1 = (adc_t / 16384.0 - (self.dig_T[0]) / 1024.0) * (self.dig_T[1])
                var2 = ((adc_t / 131072.0 - (self.dig_T[0]) / 8192.0) * (
                        adc_t / 131072.0 - (self.dig_T[0]) / 8192.0)) * (self.dig_T[2])
                t_fine = (var1 + var2)
                value = float((var1 + var2) / 5120.0)

                if -50 < value < 80:
                    bmp_temperature = round(value, 1)

                    self.bmp_temperature = bmp_temperature

                    var1 = (t_fine / 2.0) - 64000.0
                    var2 = var1 * var1 * (self.dig_P[5]) / 32768.0
                    var2 = var2 + var1 * (self.dig_P[4]) * 2.0
                    var2 = (var2 / 4.0) + ((self.dig_P[3]) * 65536.0)
                    var1 = (self.dig_P[2] * var1 * var1 / 524288.0 + self.dig_P[1] * var1) / 524288.0
                    var1 = (1.0 + var1 / 32768.0) * (self.dig_P[0])
                    p = 1048576.0 - adc_p
                    p = (p - (var2 / 4096.0)) * 6250.0 / var1
                    var1 = (self.dig_P[8]) * p * p / 2147483648.0
                    var2 = p * (self.dig_P[7]) / 32768.0
                    bmp_pressure = round((p + (var1 + var2 + (self.dig_P[6])) / 16.0) / 100, 2)

                    Storage.instance().entities().changeState(
                        'shpi', {
                            'entity_id': 'sensor.bmp_temperature',
                            'state': bmp_temperature,
                            'unit': '°C'
                        })

                    Storage.instance().entities().changeState(
                        'shpi', {
                            'entity_id': 'sensor.bmp_pressure',
                            'state': bmp_pressure,
                            'unit': 'hPa'
                        })
            except Exception as e:
                print('error BMP: {}'.format(e))

    def get_atmega_values(self):
        if self.ADDR_32U4 != 0:
            time.sleep(0.07)
            factor = 5000.0 / 1024.0 / 185.0

            try:
                atmega32u4_relay1current = factor * (self.bus.read_two_bytes(self.ADDR_32U4, self.READ_RELAY1CURRENT) - 2)
                Storage.instance().entities().changeState(
                    'shpi', {
                        'entity_id': 'sensor.atmega_relay1current',
                        'state': atmega32u4_relay1current,
                        'unit': 'A'
                    })
            except:
                print('No relay 1 current')

            atmega32u4_temperature = round(self.bus.read_two_bytes(self.ADDR_32U4, self.READ_ATMEGA_TEMP) * 0.558 - 142.5, 1)
            time.sleep(0.01)
            atmega32u4_volt = round(self.bus.read_two_bytes(self.ADDR_32U4, self.READ_ATMEGA_VOLT) / 1000, 1)
            atmega32u4_a0 = self.bus.read_two_bytes(self.ADDR_32U4, self.READ_A0)
            time.sleep(0.05)
            atmega32u4_a1 = self.bus.read_two_bytes(self.ADDR_32U4, self.READ_A1)
            atmega32u4_a2 = self.bus.read_two_bytes(self.ADDR_32U4, self.READ_A2)
            atmega32u4_a3 = self.bus.read_two_bytes(self.ADDR_32U4, self.READ_A3)
            time.sleep(0.05)
            atmega32u4_airquality = self.bus.read_two_bytes(self.ADDR_32U4, self.READ_A4)
            atmega32u4_a5 = self.bus.read_two_bytes(self.ADDR_32U4, self.READ_A5)
            atmega32u4_a7 = self.bus.read_two_bytes(self.ADDR_32U4, self.READ_A6)



            Storage.instance().entities().changeState(
                'shpi', {
                    'entity_id': 'sensor.atmega_temperature',
                    'state': atmega32u4_temperature,
                    'unit': '°C'
                })

            Storage.instance().entities().changeState(
                'shpi', {
                    'entity_id': 'sensor.atmega_volt',
                    'state': atmega32u4_volt,
                    'unit': 'V'
                })

            Storage.instance().entities().changeState(
                'shpi', {
                    'entity_id': 'sensor.atmega_airquality',
                    'state': atmega32u4_airquality,
                    'unit': '%'
                })

    def get_temperature(self):
        Storage.instance().entities().changeState(
            'shpi', {
                'entity_id': 'sensor.temperature',
                'state': (self.sht_temperature + self.bmp_temperature) / 2,
                'unit': '°C'
            })


        '''
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
        '''

    def turn_on_fan(self):
        #os.system('i2cset -y 2 0x2A 0x93 0')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'fan.main', 'state': 'on'})
        pass

    def turn_off_fan(self):
        #os.system('i2cset -y 2 0x2A 0x93 254')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'fan.main', 'state': 'off'})
        pass

    def turn_on_relay_1(self):
        #os.system('i2cset -y 2 0x2A 0x8D 0x00')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_1', 'state': 'on'})
        pass

    def turn_off_relay_1(self):
        #os.system('i2cset -y 2 0x2A 0x8D 0xFF')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_1', 'state': 'off'})
        pass

    def turn_on_relay_2(self):
        #os.system('i2cset -y 2 0x2A 0x8E 0x00')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_2', 'state': 'on'})
        pass

    def turn_off_relay_2(self):
        #os.system('i2cset -y 2 0x2A 0x8E 0xFF')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_2', 'state': 'off'})
        pass

    def turn_on_relay_3(self):
        #os.system('i2cset -y 2 0x2A 0x8F 0x00')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_3', 'state': 'on'})
        pass

    def turn_off_relay_3(self):
        #os.system('i2cset -y 2 0x2A 0x8F 0xFF')
        #Storage.instance().entities().changeState('shpi', {'entity_id': 'switch.relay_3', 'state': 'off'})
        pass

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
