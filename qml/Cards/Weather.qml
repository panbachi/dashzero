import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import "../../."

Page {
    property var card

    Pane {
        width: parent.width
        height: parent.height

        Material.elevation: 6

        Label {
            text: card.name
            font.pointSize: 25
            anchors.centerIn: parent
        }
    }
}
