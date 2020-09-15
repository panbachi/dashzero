import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtWebSockets 1.0
import ".."

ApplicationWindow {
    property var hardware
    property var config
    property var connectors
    property var entities

    id: root
    visible: true
    width: 800
    height: 480

    Material.theme: Material.Dark
    Material.accent: Material.Blue

    header: TabBar {
        id: mainNavigation
        width: parent.width
        currentIndex: mainContent.currentIndex
    }

    StackView {
        anchors.fill: parent

        SwipeView {
            id: mainContent
            currentIndex: mainNavigation.currentIndex
            anchors.fill: parent
        }
    }

    Component.onCompleted: {
        // prevent garbage collection
        hardware = Core.hardware()
        config = Core.config()
        connectors = Core.connectors()
        entities = Core.entities()

        if(Core.config().get('connectors.homeassistant')) {
            var component = Qt.createComponent("Connectors/HomeAssistant.qml");

            if (component.status == Component.Ready) {
                var connector = component.createObject(mainNavigation, {Core: Core});
                Core.connectors().set('homeassistant', connector);
            }
        }

        var button = Qt.createComponent("MainNavigationButton.qml");
        var room = Qt.createComponent("Room.qml");

        if (button.status == Component.Ready && room.status == Component.Ready) {
            var rooms = Core.config().get('rooms');

            for(var r in rooms) {
                button.createObject(mainNavigation, {subIcon: Icons.get[rooms[r].icon], Core: Core});
                room.createObject(mainContent, {room: rooms[r], Core: Core});
            }
        }
    }

    property bool sleep: false

    MouseArea {
        anchors.fill: parent
        propagateComposedEvents: true
        onPressed: {
            if(Core.hardware()) {
               Core.hardware().wakeup();
            }
            root.sleep = false;
            timer.restart();
            mouse.accepted = false;
        }
        onReleased: {
            mouse.accepted = false;
        }
    }

    Timer {
        id: timer
        interval: 5000;
        running: true;
        repeat: false
        onTriggered: {
            //Core.hardware().sleep()
            //root.sleep = true;
        }
    }
}

