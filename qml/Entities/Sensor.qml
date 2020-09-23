import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Item {
    id: item

    function update(connector, key, type, value) {
        if(connector == entity.connector && key == entity.entity_id && type == 'sensor') {
            var unit = value.unit || '';
            v.text = value.state + ' ' + unit;
        }
    }

    width: parent.width
    height: parent.height

    RowLayout  {
        width: parent.width - 30
        height: parent.height

        Label {
            id: i

            text: Icons.get[icon]
            font.family: Fonts.icon
            width: 90
            height: contentHeight
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 25
            color: "#BDC3C7"

            Layout.preferredWidth: 90
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

    Component.onCompleted: {
        Core.entities().registerEntity(entity.connector, entity.entity_id, 'sensor')
        Core.entities().changedSignal.connect(update)
    }
}