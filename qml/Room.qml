import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import "../."

Page {
    property var room

    footer: TabBar {
        id: roomNavigation
        width: parent.width
        currentIndex: roomContent.currentIndex
    }

    SwipeView {
        id: roomContent
        currentIndex: roomNavigation.currentIndex
        anchors.fill: parent
    }

    Component.onCompleted: {
        var button = Qt.createComponent("../qml/RoomNavigationButton.qml");

        if (button.status == Component.Ready) {
            var cards = room.cards;
            var card = null;

            for(var c in cards) {
                var icon = '';
                if (cards[c]['type'] == 'lights') {
                    icon = 'lightbulb';
                    card = Qt.createComponent("../qml/Cards/Lights.qml");
                } else if (cards[c]['type'] == 'entities') {
                    icon = 'lightbulb';
                    card = Qt.createComponent("../qml/Cards/Entities.qml");
                } else if (cards[c]['type'] == 'thermostat') {
                    icon = 'thermometer';
                    card = Qt.createComponent("../qml/Cards/Thermostat.qml");
                } else if (cards[c]['type'] == 'garbage') {
                    icon = 'delete-empty';
                    card = Qt.createComponent("../qml/Cards/Garbage.qml");
                } else if (cards[c]['type'] == 'weather') {
                    icon = 'weather-partly-cloudy';
                    card = Qt.createComponent("../qml/Cards/Weather.qml");
                } else if (cards[c]['type'] == 'door') {
                    icon = 'door';
                    card = Qt.createComponent("../qml/Cards/Door.qml");
                } else {
                    return;
                }

                button.createObject(roomNavigation, {text: cards[c].name, subIcon: Icons.get[icon], Core: Core});

                if(card.status == Component.Ready) {
                    card.createObject(roomContent, {card: cards[c], Core: Core});
                }
            }
        }
    }
}
