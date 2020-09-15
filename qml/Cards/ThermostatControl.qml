import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Button {
    id: c

    property var card
    property var control

    font.pointSize: 40
    font.family: Fonts.icon

    Layout.fillWidth: true
    Layout.alignment: Qt.AlignHCenter
    Layout.preferredWidth: 50

    contentItem: Text {
        text: c.text
        font: c.font
        opacity: enabled ? 1.0 : 0.3
        color: control.color
    }

    Component.onCompleted: {
        //console.log(control)
    }
}
