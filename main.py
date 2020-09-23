import os
import sys
import yaml
from PySide2.QtCore import QtInfoMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg, qInstallMessageHandler
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from core.storage import Storage
from core.hardware import Hardware
from core.config import Config
from core.entities import Entities
from core.connectors import Connectors

config = None

def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
        mode = 'Info'
    elif mode == QtWarningMsg:
        mode = 'Warning'
        #return
    elif mode == QtCriticalMsg:
        mode = 'critical'
    elif mode == QtFatalMsg:
        mode = 'fatal'
    else:
        mode = 'Debug'
    print("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file))


if __name__ == '__main__':
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']
    qInstallMessageHandler(qt_message_handler)
    app = QGuiApplication(sys_argv)
    engine = QQmlApplicationEngine()

    if os.path.exists('config.yaml'):
        config_file = 'config.yaml'
    else:
        config_file = 'config.example.yaml'

    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)

    storage = Storage()
    storage.setConfig(Config(config))
    storage.setEntities(Entities())

    connectors = Connectors()

    storage.setConnectors(connectors)
    storage.setHardware(Hardware(config))

    engine.rootContext().setContextProperty('Core', storage)

    engine.load("qml/Main.qml")



    #connectors.start()

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
