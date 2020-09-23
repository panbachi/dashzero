import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import "../../."

Page {
    property var card

    ListView {
        id: entities
        width: parent.width
        height: parent.height
        model: ListModel { id: entitiesModel }
        ScrollBar.vertical: ScrollBar {
            active: true
        }
        delegate: Component {
            Item {
                id: item

                property var value
                //property var entity

                width: entities.width
                height: 70

                Component.onCompleted: {
                    var elem = '';
                    var type = entity.type;

                    /*if (type == 'light') {
                        elem = Qt.createComponent("../Entities/Light.qml");
                    } else if (type == 'fan') {
                        elem = Qt.createComponent("../Entities/Fan.qml");
                    } else */if (type == 'sensor') {
                        elem = Qt.createComponent("../Entities/Sensor.qml");
                    } else if (type == 'switch') {
                        elem = Qt.createComponent("../Entities/Switch.qml");
                    } else {
                        return;
                    }

                    if (elem.status == Component.Ready) {
                        elem.createObject(item, {name: name, icon: icon, value: value, entity: entity, Core: Core});
                    }
                }
            }
        }

        Component.onCompleted: {
            for(var i of card.entities) {
                entitiesModel.append({name: i.name, icon: i.icon, value: 0, entity: i})
            }
        }
    }
}