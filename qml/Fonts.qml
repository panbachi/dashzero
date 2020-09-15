pragma Singleton
import QtQuick 2.12

Item {
    id: fonts

    readonly property string icon: iconFont.name

    FontLoader {
        id: iconFont
        source: "../assets/fonts/materialdesignicons-webfont.ttf"
    }
}