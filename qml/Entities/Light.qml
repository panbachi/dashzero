import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import "../../."

Item {
    property var entity

    width: parent.width
    height: parent.height

    Row {
        width: parent.width
        height: parent.height

        Label {
            id: i

            function update(connector, key, value) {
                if(connector == entity.connector && key == entity.entity_id) {
                    item.value = value.state;

                    if(value.state == 'on') {
                        i.color = "#F1C40F";
                    } else if(value.state == 'off') {
                        i.color = "#BDC3C7";
                    }
                }
            }

            text: Icons.get[icon]
            font.family: Fonts.icon
            width: 90
            height: contentHeight
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 50
            color: "#BDC3C7"

            Component.onCompleted: {
                Core.entities().changedSignal.connect(update)
            }
        }

        Label {
            text: name
            font.pointSize: 25
            height: i.height
            verticalAlignment: Text.AlignVCenter
        }
    }

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if(item.value == 'on') {
                Core.entities().setState(entity.connector, entity.entity_id, 'off');
            } else { // if(item.value == 'off') {
                Core.entities().setState(entity.connector, entity.entity_id, 'on');
            }

        }
    }
}