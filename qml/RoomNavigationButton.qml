import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import "../."

TabButton {
    id: button
    //text: "test"
    property alias subIcon: icon.text
    property int roomIndex
    property int cardIndex

    contentItem: Column {
        width: parent.width
        height: parent.height
        Label {
            id: icon
            width: parent.width
            text: parent.parent.subIcon
            font.family: Fonts.icon
            font.pointSize: 20
            horizontalAlignment: Text.AlignHCenter
        }

        Label {
            id: label
            text: qsTr(parent.parent.text)
            width: parent.width
            font.pointSize: 8
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignBottom
            //font.bold: true
            font.capitalization: Font.AllUppercase
        }
    }

}
