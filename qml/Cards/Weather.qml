import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.12
import "../../."

Page {
    property var card
    property var entity: {
        'entity_id': '',
        'condition': '',
        'condition_label': '',
        'condition_icon': '',
        'temperature': '',
        'humidity': '',
        'pressure': '',
        'wind_direction': '',
        'wind_speed': '',
        'forecast': [{
            'condition': '',
            'condition_icon': '',
            'day': '',
            'temperature': ''
        }, {
            'condition': '',
            'condition_icon': '',
            'day': '',
            'temperature': ''
        }, {
            'condition': '',
            'condition_icon': '',
            'day': '',
            'temperature': ''
        }, {
            'condition': '',
            'condition_icon': '',
            'day': '',
            'temperature': ''
        }, {
            'condition': '',
            'condition_icon': '',
            'day': '',
            'temperature': ''
        }]
    }

    function update(connector, key, type, value) {
        if(connector == card.connector && key == card.entity_id && type == 'weather') {
            entity = value
        }
    }

    Label {
        text: entity.condition_label
        font.pointSize: 30
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        x: 0
        y: 0
        width: parent.width
        height: 75
    }

    Label {
        text: entity.condition_icon ? Icons.get[entity.condition_icon] : ''
        font.family: Fonts.icon
        color: Material.color(Material.Blue)
        font.pointSize: 80
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        x: 0
        y: 75
        width: parent.width * 0.17
        height: 150
    }

    Label {
        textFormat: Text.RichText
        text: entity.temperature + '<sup style="font-size: 70px">°C</sup>'
        font.pointSize: 60
        font.weight: Font.Light
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        x: parent.width * 0.17
        y: 75
        width: parent.width * 0.35
        height: 150
    }

    Column {
        id: col
        x: (parent.width * 0.20) + (parent.width * 0.35)
        y: 75
        width: parent.width * 0.45
        height: 150

        Label {
            text: "Luftfeuchtigkeit: " + entity.humidity + "%"
            font.pointSize: 13
            height: 50
            verticalAlignment: Text.AlignVCenter
        }
        Label {
            text: "Luftdruck: " + entity.pressure + " hPa"
            font.pointSize: 13
            height: 50
            verticalAlignment: Text.AlignVCenter
        }
        Label {
            text: "Windgeschwindigkeit: " + entity.wind_speed + " km/h (" + entity.wind_direction + ")"
            font.pointSize: 13
            height: 50
            verticalAlignment: Text.AlignVCenter
        }
    }

    Pane {
        id: row
        height: 130
        width: parent.width
        x: 0
        y: 225

        GridLayout {

            anchors.fill: parent
            columns: 5

            ColumnLayout {
                Label {
                    text: entity.forecast[0].day
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[0].condition_icon ? Icons.get[entity.forecast[0].condition_icon] : ''
                    font.family: Fonts.icon
                    font.pointSize: 30
                    color: Material.color(Material.Blue)
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[0].temperature + "°C"
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            ColumnLayout {
                Label {
                    text: entity.forecast[1].day
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[1].condition_icon ? Icons.get[entity.forecast[0].condition_icon] : ''
                    font.family: Fonts.icon
                    font.pointSize: 30
                    color: Material.color(Material.Blue)
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[1].temperature + "°C"
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            ColumnLayout {
                Label {
                    text: entity.forecast[2].day
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[2].condition_icon ? Icons.get[entity.forecast[0].condition_icon] : ''
                    font.family: Fonts.icon
                    font.pointSize: 30
                    color: Material.color(Material.Blue)
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[2].temperature + "°C"
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            ColumnLayout {
                Label {
                    text: entity.forecast[3].day
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[3].condition_icon ? Icons.get[entity.forecast[0].condition_icon] : ''
                    font.family: Fonts.icon
                    font.pointSize: 30
                    color: Material.color(Material.Blue)
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[3].temperature + "°C"
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            ColumnLayout {
                Label {
                    text: entity.forecast[4].day
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[4].condition_icon ? Icons.get[entity.forecast[0].condition_icon] : ''
                    font.family: Fonts.icon
                    font.pointSize: 30
                    color: Material.color(Material.Blue)
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }

                Label {
                    text: entity.forecast[4].temperature + "°C"
                    Layout.fillWidth: true
                    font.pointSize: 13
                    horizontalAlignment: Text.AlignHCenter
                }
            }


        }
    }

    Component.onCompleted: {
        Core.entities().registerEntity(card.connector, card.entity_id, 'weather')
        Core.entities().changedSignal.connect(update);
    }
}
