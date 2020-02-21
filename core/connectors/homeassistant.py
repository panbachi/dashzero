# -*- coding: utf-8 -*-
import json
from kivy.support import install_twisted_reactor

install_twisted_reactor()
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
from twisted.internet import reactor


class HAClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        self.factory.handler.print_message('WebSocket connection open.')
        self.factory._proto = self

        self.sendMessage(json.dumps(
            {'type': 'auth',
             'access_token': self.config['access_token']}
        ).encode('utf8'), isBinary=False)

        self.sendMessage(json.dumps(
            {'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}
        ).encode('utf8'), isBinary=False)

        self.sendMessage(json.dumps(
            {'id': 2, 'type': 'get_states'}
        ).encode('utf8'), isBinary=False)

    def onMessage(self, payload, is_binary):
        if is_binary:
            self.factory.handler.print_message("Binary message received: {0} bytes".format(len(payload)))
        else:
            self.factory.handler.print_message("Got from server: {}".format(payload.decode('utf8')))
            self.factory.handler.handle_message(json.loads(payload.decode('utf8')))

    def onClose(self, was_clean, code, reason):
        self.factory.handler.print_message("WebSocket connection closed: {0}".format(reason))
        self.factory._proto = None


class HAClientFactory(WebSocketClientFactory):
    protocol = HAClientProtocol

    def __init__(self, config, handler):
        url = 'ws://' + config['host'] + ':' + str(config['port']) + '/api/websocket'
        WebSocketClientFactory.__init__(self, url)

        self.handler = handler
        # Not sure why/whether _proto is needed?
        self._proto = None
        self.protocol.config = config


class HomeAssistant:
    def __init__(self, app, config):
        self.config = config
        self.app = app
        self.ws_count = 2
        self._factory = None

    def connect_to_server(self):
        self._factory = HAClientFactory(self.config, self)
        reactor.connectTCP(self.config['host'], self.config['port'], self._factory)

    def send_message(self, msg):
        proto = self._factory._proto
        if proto:
            proto.sendMessage(msg, isBinary=False)

            self.print_message('Sent to server: {}')

    def print_message(self, msg):
        print(str(msg) + '\n')

    def handle_message(self, msg):
        if msg['type'] == 'event':
            self.app.dispatch('on_state_changed', msg['event']['data']['new_state'])

        if msg['type'] == 'result' and msg['id'] == 2:
            for result in msg['result']:
                if 'camera' in result['entity_id'].split('.')[0]:
                    result['attributes']['entity_picture'] = 'http://' + self.config['host'] + ':' + str(
                        self.config['port']) + result['attributes']['entity_picture']

                self.app.dispatch('on_state_changed', result)

    def change_state(self, entity_id, state):
        service = 'turn_on'

        if state == 'off':
            service = 'turn_off'

        domain = entity_id.split('.')[0]

        self.ws_count = self.ws_count + 1

        self.send_message(json.dumps({
            "id": self.ws_count,
            "type": "call_service",
            "domain": domain,
            "service": service,
            "service_data": {
                "entity_id": entity_id
            }
        }).encode('utf8'))

        return True

    def change_temperature(self, entity_id, temperature):
        self.ws_count = self.ws_count + 1

        self.send_message(json.dumps({
            "id": self.ws_count,
            "type": "call_service",
            "domain": 'climate',
            "service": 'set_temperature',
            "service_data": {
                "entity_id": entity_id,
                "temperature": temperature
            }
        }).encode('utf8'))

        return True
