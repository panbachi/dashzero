import QtQuick 2.12
import QtWebSockets 1.0
import "../../."

WebSocket {
    id: socket

    property int count
    property var config
    property var entities

    function setState(entityId, state) {
        count = count + 1;

        var service = 'turn_' + state;

        var domain = entityId.split('.')[0];

        socket.sendTextMessage(JSON.stringify({
            "id": count,
            "type": "call_service",
            "domain": domain,
            "service": service,
            "service_data": {
                "entity_id": entityId
            }
        }))
    }

    url: "ws://" + config.host + ":" + config.port + '/api/websocket'
    active: false

    onTextMessageReceived: {
        message = JSON.parse(message);

        if(message.type == 'event') {
            var state = {
                entity_id: message.event.data.new_state.entity_id,
            };

            if(message.event.data.new_state.attributes.unit_of_measurement) {
                state.unit = message.event.data.new_state.attributes.unit_of_measurement;
            }

            if(message.event.data.new_state.state && message.event.data.new_state.state != 'unknown') {
                state.state = message.event.data.new_state.state;
            } else if(message.event.data.new_state.attributes.temperature) {
                state.state = message.event.data.new_state.attributes.temperature;
            }

            entities.changeState('homeassistant', state)
        }

        if(message.type == 'result' && message.id == 2) {
            for(var result of message.result) {
                var state = {
                    entity_id: result.entity_id,
                };

                if(result.attributes.unit_of_measurement) {
                    state.unit = result.attributes.unit_of_measurement;
                }

                if(result.state && result.state != 'unknown') {
                    state.state = result.state;
                } else if(result.attributes.temperature) {
                    state.state = result.attributes.temperature;
                }

                var type = result.entity_id.split('.')[0];
                if(type.indexOf('camera') >= 0) {
                    state.picture = 'http://' + config.host + ':' + config.port + result.attributes.entity_picture;
                }

                entities.changeState('homeassistant', state);
            }
        }
    }

    onStatusChanged: {
        if (socket.status == WebSocket.Error) {
            console.log("Error: " + socket.errorString)
        } else if (socket.status == WebSocket.Open) {
            socket.sendTextMessage(JSON.stringify({
                'type': 'auth',
                'access_token': config.access_token
            }));

            socket.sendTextMessage(JSON.stringify({
                'id': 1,
                'type': 'subscribe_events',
                'event_type': 'state_changed'
            }));

            socket.sendTextMessage(JSON.stringify({
                'id': 2,
                'type': 'get_states'
            }));

        } else if (socket.status == WebSocket.Closed) {
            console.log("Socket closed")
        }
    }

    Component.onCompleted: {
        socket.entities = Core.entities()
        socket.count = 2;
        socket.active = true;
        socket.config = Core.config().get('connectors.homeassistant');
    }
}