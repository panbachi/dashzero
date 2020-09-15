import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import "../../."

Page {
    property var card

    ListView {
        id: entities

        width: parent.width
        height: parent.height
        model: ListModel { id: entitiesModel }

        ScrollBar.vertical: ScrollBar {
            active: true
        }

        delegate: Component {
            Item {
                property var value

                id: item
                width: parent.width
                height: 110


                Row {
                    width: parent.width

                    Label {
                        id: i

                        function update(connector, key, value) {
                            if(connector == entity.connector && key == entity.entity_id) {
                                item.value = value.state;

                                if(value.state == 'on') {
                                    i.color = "#F1C40F";
                                } else if(value.state == 'off') {
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
                        font.pointSize: 50
                        color: "#BDC3C7"

                        Component.onCompleted: {
                            Core.entities().changedSignal.connect(update)
                        }
                    }
                    Label {
                        text: name
                        font.pointSize: 25
                        height: i.height
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                MouseArea {
                    anchors.fill: parent

                    onClicked: {
                        if(item.value == 'on') {
                            Core.entities().setState(entity.connector, entity.entity_id, 'off');
                        } else { // if(item.value == 'off') {
                            Core.entities().setState(entity.connector, entity.entity_id, 'on');
                        }

                    }
                }
            }
        }

        Component.onCompleted: {
            for(var i of card.entities) {
                entitiesModel.append({name: i.name, icon: i.icon, value: 0, entity: i})
            }
        }
    }
}