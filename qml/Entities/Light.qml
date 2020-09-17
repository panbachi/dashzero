import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.0
import "../../."

Item {
    id: item

    property var entity

    width: parent.width
    height: parent.height

    /*
    ColorDialog {
        id: colorDialog
        title: qsTr("Please choose a color")
        onAccepted: {
            console.log("You chose: " + colorDialog.color)
            //Core.entities().setColor(entity.connector, entity.entity_id, colorDialog.color);
        }
        onRejected: {
            console.log("Canceled")
        }
        Component.onCompleted: visible = false
    }*/

    RowLayout  {
        width: parent.width - 30
        height: parent.height

        Label {
            id: i

            function update(connector, key, value) {
                if(connector == entity.connector && key == entity.entity_id) {
                    if(value.state == 'on') {
                        v.checked = true;
                        i.color = "#F1C40F";
                    } else {
                        v.checked = false;
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
            font.pointSize: 25
            color: "#BDC3C7"

            Layout.preferredWidth: 90

            /*MouseArea {
                anchors.fill: parent

                onClicked: {
                    console.log(colorDialog)
                    colorDialog.visible = true
                }

            }*/


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

            /*MouseArea {
                anchors.fill: parent

                onPressAndHold: {
                    console.log('OPEN MODAL');
                    popup.open();
                }
            }*/
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

/*
    Popup {
        id: popup
        width: item.parent.parent.parent.width - 100
        height: item.parent.parent.parent.height

        modal: true
        focus: true
        anchors.centerIn: Overlay.overlay
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        Column {

            Button {
                text: qsTr("Choose color")

                onClicked: {
                    colorDialog.color = '#123456';
                    colorDialog.visible = true
                }
            }

            Slider {
                from: 1
                value: 25
                to: 100
            }
        }
    }*/
}