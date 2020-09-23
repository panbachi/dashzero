import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Page {
    property var card
    property var config

    Pane {
        width: parent.width
        height: parent.height

        Material.elevation: 6

        Label {
            id: label

            property var unit

            function update(connector, key, type, value) {
                if(connector == card.connector && key == card.entity_id && type == 'climate') {
                    var temperature = '°C';
                    if(unit == 'fahrenheit') {
                        temperature = '°F';
                    }

                    text = value.state + '<sup style="font-size: 80px">' + temperature + '</sup>';
                }
            }

            text: ""
            x: 0
            y: 100
            width: 300
            height: 120
            font.pointSize: 90
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            textFormat: Text.RichText

            Component.onCompleted: {
                Core.entities().registerEntity(card.connector, card.entity_id, 'climate')
                unit = config.get('core.temperature')
                Core.entities().changedSignal.connect(update)
            }
        }

        Button {
            text: Icons.get['minus']
            font.family: Fonts.icon
            x: 0
            y: 220
            width: 300
            height: 100
            font.pointSize: 80
            flat: true

            Material.foreground: Material.Blue

            onClicked: {
                console.log('Minus')
            }
        }

        Button {
            text: Icons.get['plus']
            font.family: Fonts.icon
            x: 0
            y: 0
            width: 300
            height: 100
            font.pointSize: 80
            flat: true
            Material.foreground: Material.Red

            onClicked: {
                console.log('Plus')
            }
        }

        ListView {
            id: sensors

            x: 350
            y: 0
            width: 450
            height: 200
            model: ListModel { id: sensorsModel }

            ScrollBar.vertical: ScrollBar {
                active: true
            }

            delegate: Component {
                Item {
                    width: 180
                    height: 70

                    Column {
                        width: parent.width

                        Row {
                            Label {
                                text: Icons.get[icon]
                                font.family: Fonts.icon
                                width: 100
                                height: parent.height
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                                font.pointSize: 20
                            }
                            Column {
                                Label {
                                    text: name
                                    font.pointSize: 12
                                }

                                Label {
                                    id: val

                                    function update(connector, key, type, value) {
                                        if(connector == sensor.connector && key == sensor.entity_id && type == 'sensor') {
                                            val.text = value.state + ' ' + value.unit;
                                        }
                                    }

                                    text: ''
                                    font.pointSize: 12

                                    Component.onCompleted: {
                                        Core.entities().registerEntity(sensor.connector, sensor.entity_id, 'sensor')
                                        Core.entities().changedSignal.connect(update)
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Component.onCompleted: {
                for(var i of card.sensors) {
                    sensorsModel.append({name: i.name, icon: i.icon, value: 0, sensor: i})
                }
            }
        }

        RowLayout {
            id: newControls

            x: 360
            y: 250
            width: 440
            height: 100
            spacing: 2
            Layout.alignment: Qt.AlignHCenter

            Component.onCompleted: {
                var button = Qt.createComponent("./ThermostatControl.qml");

                if (button.status == Component.Ready) {
                    for(var i of card.controls) {
                        button.createObject(newControls, {text: Icons.get[i.icon], flat: true, control: i, card: card});
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        config = Core.config();
        Core.entities().registerEntity(card.connector, card.entity_id, 'climate')
    }
}
