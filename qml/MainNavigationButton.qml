import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import "../."

TabButton {
    id: button
    property alias subIcon: button.text
    property int roomIndex
    text: button.subIcon
    font.family: Fonts.icon
    font.pointSize: 25
}
