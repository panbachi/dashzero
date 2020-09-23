import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Page {
    property var card

    ListModel { id: entitiesModel }

    GridLayout {
        id: grid

        anchors.fill: parent // GridLayout must have the right size now
        anchors.margins: 10
        //rows: 3
        columns: 5
        columnSpacing: 10
        rowSpacing: 10
        //spacing: 6
        //horizontalItemAlignment: Grid.AlignHCenter
        //verticalItemAlignment: Grid.AlignVCenter
        //width: parent.width
        //height: parent.height


        //Layout.margins: 50
        Layout.leftMargin: 50
        Layout.topMargin: 50
        Layout.rightMargin: 50
        Layout.bottomMargin: 50

        Repeater {
            id: repeater;
            model: entitiesModel
            //model: 9

            delegate: Component {

                Item {
                    id: item

                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    Component.onCompleted: {
                        var elem = '';
                        var type = entity.type;

                        /*if (type == 'light') {
                            elem = Qt.createComponent("../EntitiesGrid/Light.qml");
                        } else if (type == 'fan') {
                            elem = Qt.createComponent("../EntitiesGrid/Fan.qml");
                        } else */if (type == 'sensor') {
                            elem = Qt.createComponent("../EntitiesGrid/Sensor.qml");
                        } else if (type == 'switch') {
                            elem = Qt.createComponent("../EntitiesGrid/Switch.qml");
                        } else {
                            return;
                        }

                        if (elem.status == Component.Ready) {
                            elem.createObject(item, {name: name, icon: icon, value: value, entity: entity, Core: Core});
                        }
                    }
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
