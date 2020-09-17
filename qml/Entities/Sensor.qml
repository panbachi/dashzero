import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Item {
    id: item

    width: parent.width
    height: parent.height

    RowLayout  {
        width: parent.width - 30
        height: parent.height

        Label {
            id: i

            function update(connector, key, value) {
                if(connector == entity.connector && key == entity.entity_id) {
                    var unit = value.unit || '';
                    v.text = value.state + ' ' + unit;
                }
            }

            text: Icons.get[icon]
            font.family: Fonts.icon
            width: 90
            height: contentHeight
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 25
            color: "#BDC3C7"

            Layout.preferredWidth: 90

            Component.onCompleted: {
                Core.entities().changedSignal.connect(update)
            }
        }

        Label {
            Layout.fillWidth: true
            text: name
            font.pointSize: 20
            height: i.height
            verticalAlignment: Text.AlignVCenter
        }

        Label {
            id: v

            text: ''
            font.pointSize: 15
            height: i.height
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignRight
        }
    }
}