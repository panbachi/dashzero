import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtMultimedia 5.0
import QtWebView 1.0
import "../../."

Page {
    property var card

    Rectangle {
        id: video

        property int imageVisible: 1
        property string initialSource
        property int counter: 0

        function update(connector, key, type, value) {
            if(connector == card.camera.connector && key == card.camera.entity_id && type == 'camera') {
                video.initialSource = value.picture
                setSource(video.initialSource)
            }
        }

        function setSource(source){
            counter = counter + 1;

            if(counter > 2) {
                counter = 0;
            }

            var imageNew = imageVisible === 1 ? image2 : image1;
            var imageOld = imageVisible === 2 ? image2 : image1;

            imageNew.source = source + '&' + counter;

            function finishImage(){
                if(imageNew.status === Component.Ready) {
                    imageNew.statusChanged.disconnect(finishImage);
                    imageVisible = imageVisible === 1 ? 2 : 1;
                    setSource(video.initialSource);
                }
            }

            if (imageNew.status === Component.Loading){
                imageNew.statusChanged.connect(finishImage);
            }
            else {
                finishImage();
            }
        }

        color: "transparent"
        width: parent.width
        height: parent.height

        Image {
            id: image1

            height: parent.height
            width: parent.width - 200
            fillMode: Image.PreserveAspectFit
            clip: true
            cache: false
            visible: video.imageVisible === 1
            source: video.initialSource
        }

        Image {
            id: image2

            height: parent.height
            width: parent.width - 200
            fillMode: Image.PreserveAspectFit
            clip: true
            cache: false
            visible: video.imageVisible === 2
        }

        Component.onCompleted: {
            Core.entities().registerEntity(card.camera.connector, card.camera.entity_id, 'camera')
            Core.entities().changedSignal.connect(update);
        }

        Label {
            id: button

            property string state

            function update(connector, key, type, value) {
                if(connector == card.opener.connector && key == card.opener.entity_id) {
                    button.state = value.state;

                    if(value.state == 'on') {
                        button.color = "#27AE60";
                        button.text = Icons.get['door-open']
                    } else if(value.state == 'off') {
                        button.color = "#C0392B";
                        button.text = Icons.get['door-closed']
                    }
                }
            }

            text: ''
            font.family: Fonts.icon
            width: 200
            height: parent.height
            x: 600
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pointSize: 120

            Component.onCompleted: {
                Core.entities().registerEntity(card.opener.connector, card.opener.entity_id, 'switch')
                Core.entities().changedSignal.connect(update);
            }

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    if(button.state == 'on') {
                        Core.entities().setState(card.opener.connector, card.opener.entity_id, 'off');
                    } else if(button.state == 'off') {
                        Core.entities().setState(card.opener.connector, card.opener.entity_id, 'on');
                    }
                }
            }
        }
    }
}
