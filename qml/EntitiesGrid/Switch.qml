import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Pane {
    id: item

    property var entity
    property var state


    function update(connector, key, type, value) {
        if(connector == entity.connector && key == entity.entity_id && type == 'switch') {
            item.state = value.state

            if(value.state == 'on') {
                i.color = "#F1C40F";
            } else {
                i.color = "#BDC3C7";
            }
        }
    }

    width: parent.width
    height: parent.height


    Material.elevation: 1
    //Material.background: Material.color(Material.Red, Material.Shade800)

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if(item.state == 'off') {
                Core.entities().setState(entity.connector, entity.entity_id, 'switch', 'on');
            } else { // if(item.value == 'off') {
                Core.entities().setState(entity.connector, entity.entity_id, 'switch', 'off');
            }
        }

    }

    ColumnLayout{
        anchors.fill: parent
        Layout.fillHeight: true
        Layout.fillWidth: true


        Label {
            id: n
            text: name
            Layout.alignment: Qt.AlignTop
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignTop
        }

        Label {
            id: i
            Layout.fillHeight: true
            Layout.fillWidth: true
            text: Icons.get[icon]
            font.family: Fonts.icon
            font.pointSize: 35
            color: "#BDC3C7"
            Layout.alignment: Qt.AlignTop
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter

        }

        Label {
            id: placeholder
            text: ''
            Layout.alignment: Qt.AlignBottom
        }
    }



    Component.onCompleted: {
        Core.entities().registerEntity(entity.connector, entity.entity_id, 'switch')
        Core.entities().changedSignal.connect(update)

        if(entity.bgcolor) {
            Material.background = entity.bgcolor;
        } else if(root.Material.theme == 1) {
            //Material.background = '#606060';
        }
    }
}