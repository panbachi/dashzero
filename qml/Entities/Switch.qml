import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Item {
    id: item

    property var entity

    width: parent.width
    height: parent.height

    RowLayout  {
        width: parent.width - 30
        height: parent.height

        Label {
            id: i

            function update(connector, key, value) {
                if(connector == entity.connector && key == entity.entity_id) {
                    if(value.state == 'on') {
                        v.checked = true;
                    } else {
                        v.checked = false;
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

            Layout.preferredWidth: 90

            Component.onCompleted: {
                Core.entities().changedSignal.connect(update)
            }
        }

        Label {
            Layout.fillWidth: true
            text: name
            font.pointSize: 25
            height: i.height
            verticalAlignment: Text.AlignVCenter
        }

        Switch {
            id: v

            text: ''

            onToggled: {
                if(checked == true) {
                    Core.entities().setState(entity.connector, entity.entity_id, 'on');
                } else { // if(item.value == 'off') {
                    Core.entities().setState(entity.connector, entity.entity_id, 'off');
                }
            }
        }
    }
}