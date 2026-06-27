import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs

ApplicationWindow {
    id: rootWindow
    visible: true
    width: 1200
    height: 800
    title: "Secure Drive"
    color: "#0a0e17" // Dark background
    
    property int currentTabIndex: 0
    
    onCurrentTabIndexChanged: {
        if (currentTabIndex === 2) {
            scanLogsArea.text = backend.get_threat_logs()
        } else if (currentTabIndex === 3) {
            var files = JSON.parse(backend.get_quarantined_files())
            quarantineModel.clear()
            for (var i = 0; i < files.length; i++) {
                quarantineModel.append(files[i])
            }
        }
    }

    FileDialog {
        id: fileDialog
        title: "Select File to Scan"
        onAccepted: {
            backend.scan_specific_file(fileDialog.currentFile || fileDialog.fileUrl)
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // 1. Sidebar
        Rectangle {
            Layout.preferredWidth: 250
            Layout.fillHeight: true
            color: "#0a0e17"

            // Border on the right
            Rectangle {
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: 1
                color: "#1e2430"
            }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15

                // Logo
                RowLayout {
                    spacing: 10
                    Image {
                        source: "file:///" + backend.project_root + "/Logo - Secure Drive.png"
                        sourceSize.width: 40
                        sourceSize.height: 40
                        fillMode: Image.PreserveAspectFit
                    }
                    ColumnLayout {
                        spacing: 2
                        Text {
                            text: "Secure Drive"
                            color: "white"
                            font.pixelSize: 18
                            font.bold: true
                        }
                        Text {
                            text: "Your Data, Our Priority"
                            color: "#8e99ab"
                            font.pixelSize: 12
                        }
                    }
                }

                Item { height: 20 } // Spacer

                // Navigation Items
                Repeater {
                    model: ["Home", "Protection", "Scan", "Quarantine", "Notifications", "Settings", "About"]
                    delegate: Rectangle {
                        Layout.fillWidth: true
                        height: 45
                        color: index === rootWindow.currentTabIndex ? "#1e5af6" : "transparent"
                        radius: 8

                        // Glow effect for selected tab
                        Rectangle {
                            anchors.fill: parent
                            color: "#1e5af6"
                            opacity: index === rootWindow.currentTabIndex ? 0.2 : 0
                            radius: 8
                            scale: 1.1
                            z: -1
                        }

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            Text {
                                text: modelData
                                color: index === rootWindow.currentTabIndex ? "white" : "#8e99ab"
                                font.pixelSize: 14
                                font.bold: index === rootWindow.currentTabIndex
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: rootWindow.currentTabIndex = index
                            hoverEnabled: true
                            onEntered: parent.color = index === rootWindow.currentTabIndex ? "#1e5af6" : "#121824"
                            onExited: parent.color = index === rootWindow.currentTabIndex ? "#1e5af6" : "transparent"
                        }
                    }
                }

                Item { Layout.fillHeight: true } // Spacer pushes everything up

                // System Status Widget
                Rectangle {
                    Layout.fillWidth: true
                    height: 90
                    color: "#121824"
                    radius: 12
                    border.color: "#1e2430"
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 15
                        Rectangle {
                            width: 40
                            height: 40
                            radius: 20
                            color: "#0f3621"
                            Text {
                                text: "✔️"
                                anchors.centerIn: parent
                                color: "#22c55e"
                            }
                        }
                        ColumnLayout {
                            spacing: 4
                            Text { text: "System Status"; color: "#8e99ab"; font.pixelSize: 12 }
                            Text { text: "Protected"; color: "#22c55e"; font.pixelSize: 16; font.bold: true }
                            Text { text: "Everything running smoothly"; color: "#8e99ab"; font.pixelSize: 10; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                        }
                    }
                }
            }
        }

        // 2. Main Content Area (Pages)
        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: rootWindow.currentTabIndex

            // Page 0: Home
            Rectangle {
                color: "#0a0e17"
                Flickable {
                    anchors.fill: parent
                    contentWidth: parent.width
                    contentHeight: mainColumn.height + 40
                    clip: true

                    ColumnLayout {
                        id: mainColumn
                        anchors.top: parent.top
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.margins: 30
                        spacing: 25

                        // Header
                        RowLayout {
                            Layout.fillWidth: true
                            ColumnLayout {
                                spacing: 5
                                Text { text: "Welcome back! 👋"; color: "white"; font.pixelSize: 28; font.bold: true }
                                Text { text: "Your system is protected and secure."; color: "#8e99ab"; font.pixelSize: 16 }
                            }
                            Item { Layout.fillWidth: true } // Spacer
                            
                            // Realtime Protection Toggle Header
                            Rectangle {
                                width: 200
                                height: 40
                                radius: 20
                                color: "#121824"
                                border.color: "#1e2430"
                                border.width: 1
                                RowLayout {
                                    anchors.centerIn: parent
                                    Rectangle { width: 8; height: 8; radius: 4; color: backend.realtime_enabled ? "#22c55e" : "#ef4444" }
                                    Text { text: "Real-time protection"; color: "white"; font.pixelSize: 12 }
                                    Switch {
                                        checked: backend.realtime_enabled
                                        onCheckedChanged: {
                                            if (checked !== backend.realtime_enabled) {
                                                backend.toggle_realtime(checked)
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Stat Cards
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 20

                            // Card 1
                            Rectangle {
                                Layout.fillWidth: true
                                height: 120
                                color: "#121824"
                                radius: 12
                                border.color: "#1e2430"
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 20
                                    Text { text: "Protection"; color: "#8e99ab" }
                                    Text { text: backend.realtime_enabled ? "Active" : "Disabled"; color: "white"; font.pixelSize: 24; font.bold: true }
                                    Text { text: "Real-time protection status"; color: "#8e99ab"; font.pixelSize: 12 }
                                }
                            }
                            // Card 2
                            Rectangle {
                                Layout.fillWidth: true
                                height: 120
                                color: "#121824"
                                radius: 12
                                border.color: "#1e2430"
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 20
                                    Text { text: "Last Status"; color: "#8e99ab" }
                                    Text { text: "Updates"; color: "white"; font.pixelSize: 24; font.bold: true }
                                    Text { text: backend.backend_status; color: "#8e99ab"; font.pixelSize: 12; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                                }
                            }
                            // Card 3
                            Rectangle {
                                Layout.fillWidth: true
                                height: 120
                                color: "#121824"
                                radius: 12
                                border.color: "#1e2430"
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 20
                                    Text { text: "Threats Blocked"; color: "#8e99ab" }
                                    Text { text: backend.threats_blocked; color: "white"; font.pixelSize: 24; font.bold: true }
                                }
                            }
                        }

                        // Two Column Layout
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 20

                            // Quick Scan Box
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredWidth: 2
                                height: 300
                                color: "#121824"
                                radius: 12
                                border.color: "#1e2430"
                                
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 25
                                    Text { text: "System Scan"; color: "white"; font.bold: true; font.pixelSize: 18 }
                                    
                                    Item { Layout.fillHeight: true }
                                    
                                    Button {
                                        text: "Start Full System Scan"
                                        Layout.alignment: Qt.AlignHCenter
                                        Layout.preferredWidth: 200
                                        height: 45
                                        background: Rectangle {
                                            color: "#1e5af6"
                                            radius: 22
                                            Rectangle { // Inner glow
                                                anchors.fill: parent; radius: 22; color: "white"; opacity: 0.1
                                            }
                                        }
                                        contentItem: Text {
                                            text: parent.text
                                            color: "white"
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        onClicked: backend.start_full_scan()
                                    }
                                    
                                    Item { height: 10 }
                                    
                                    Button {
                                        text: "Scan Specific File"
                                        Layout.alignment: Qt.AlignHCenter
                                        Layout.preferredWidth: 200
                                        height: 45
                                        background: Rectangle {
                                            color: "#2a3441"
                                            radius: 22
                                        }
                                        contentItem: Text {
                                            text: parent.text
                                            color: "white"
                                            font.bold: true
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                        onClicked: fileDialog.open()
                                    }
                                    Item { Layout.fillHeight: true }
                                }
                            }

                            // Firewall Status
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredWidth: 3
                                height: 300
                                color: "#121824"
                                radius: 12
                                border.color: "#1e2430"
                                
                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 25
                                    Text { text: "Firewall Status"; color: "white"; font.bold: true; font.pixelSize: 18 }
                                    
                                    Item { Layout.fillHeight: true }
                                    
                                    Text { 
                                        text: "🧱"; 
                                        font.pixelSize: 64; 
                                        Layout.alignment: Qt.AlignHCenter; 
                                        opacity: 0.5 
                                    }
                                    
                                    Item { height: 10 }
                                    
                                    Text { 
                                        text: "Offline / Coming Soon"; 
                                        color: "#ef4444"; 
                                        font.bold: true; 
                                        font.pixelSize: 20; 
                                        Layout.alignment: Qt.AlignHCenter 
                                    }
                                    
                                    Text { 
                                        text: "Advanced network monitoring and traffic control will be available in a future update."; 
                                        color: "#8e99ab"; 
                                        horizontalAlignment: Text.AlignHCenter;
                                        wrapMode: Text.WordWrap;
                                        Layout.alignment: Qt.AlignHCenter;
                                        Layout.maximumWidth: 300;
                                    }
                                    
                                    Item { Layout.fillHeight: true }
                                }
                            }
                        }
                    }
                }
            }

            // Page 1: Protection
            Rectangle {
                color: "#0a0e17"
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 30
                    spacing: 20
                    
                    Text { text: "Protection Modules"; color: "white"; font.pixelSize: 24; font.bold: true }
                    
                    Item { height: 10 }
                    
                    ColumnLayout {
                        spacing: 20
                        Layout.fillWidth: true
                        
                        // Real-time Protection Card
                        Rectangle {
                            Layout.fillWidth: true
                            height: 100
                            color: "#121824"
                            radius: 12
                            border.color: "#1e2430"
                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 20
                                Text { text: "🛡️"; font.pixelSize: 32 }
                                Item { width: 10 }
                                ColumnLayout {
                                    Text { text: "Real-Time Protection"; color: "white"; font.bold: true; font.pixelSize: 18 }
                                    Text { text: "Continuously monitors your system and instantly blocks incoming threats."; color: "#8e99ab" }
                                }
                                Item { Layout.fillWidth: true }
                                Switch { 
                                    checked: backend.realtime_enabled
                                    onCheckedChanged: {
                                        if (checked !== backend.realtime_enabled) {
                                            backend.toggle_realtime(checked)
                                        }
                                    }
                                }
                            }
                        }
                        
                        // Firewall Protection Card (Placeholder)
                        Rectangle {
                            Layout.fillWidth: true
                            height: 100
                            color: "#121824"
                            radius: 12
                            border.color: "#1e2430"
                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 20
                                Text { text: "🧱"; font.pixelSize: 32; opacity: 0.5 }
                                Item { width: 10 }
                                ColumnLayout {
                                    Text { text: "Firewall Protection (Coming Soon)"; color: "#a0aabf"; font.bold: true; font.pixelSize: 18 }
                                    Text { text: "Monitor and control incoming and outgoing network traffic."; color: "#6b7280" }
                                }
                                Item { Layout.fillWidth: true }
                                Switch { 
                                    enabled: false
                                    checked: false
                                }
                            }
                        }
                    }
                    
                    Item { Layout.fillHeight: true }
                }
            }

            // Page 2: Scan (Logs & Actions)
            Rectangle {
                id: scanPageContainer
                color: "#0a0e17"
                
                property int innerIndex: 0
                
                onVisibleChanged: {
                    if (visible) {
                        scanPageContainer.innerIndex = 0
                    }
                }

                StackLayout {
                    anchors.fill: parent
                    currentIndex: scanPageContainer.innerIndex
                    
                    // 2a: Available Scans View
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 30
                        
                        RowLayout {
                            Layout.fillWidth: true
                            Text { text: "Available Scans"; color: "white"; font.pixelSize: 24; font.bold: true; Layout.fillWidth: true }
                            Button {
                                text: "Logs"
                                Layout.preferredWidth: 100
                                height: 35
                                background: Rectangle { color: "#2a3441"; radius: 5 }
                                contentItem: Text { text: parent.text; color: "white"; font.bold: true; horizontalAlignment: Text.AlignHCenter }
                                onClicked: {
                                    scanLogsArea.text = backend.get_threat_logs()
                                    scanPageContainer.innerIndex = 1
                                }
                            }
                        }
                        
                        Item { height: 20 }
                        
                        ColumnLayout {
                            spacing: 20
                            Layout.fillWidth: true
                            
                            // Full Scan Card
                            Rectangle {
                                Layout.fillWidth: true
                                height: 100
                                color: "#121824"
                                radius: 12
                                border.color: "#1e2430"
                                RowLayout {
                                    anchors.fill: parent
                                    anchors.margins: 20
                                    Text { text: "🔍"; font.pixelSize: 32 }
                                    Item { width: 10 }
                                    ColumnLayout {
                                        Text { text: "Full System Scan"; color: "white"; font.bold: true; font.pixelSize: 18 }
                                        Text { text: "Thoroughly check all files and folders for hidden threats."; color: "#8e99ab" }
                                    }
                                    Item { Layout.fillWidth: true }
                                    Button {
                                        text: "Scan Now"
                                        Layout.preferredWidth: 120
                                        height: 40
                                        background: Rectangle { color: "#1e5af6"; radius: 6 }
                                        contentItem: Text { text: parent.text; color: "white"; font.bold: true; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                        onClicked: backend.start_full_scan()
                                    }
                                }
                            }
                            
                            // Specific File Scan Card
                            Rectangle {
                                Layout.fillWidth: true
                                height: 100
                                color: "#121824"
                                radius: 12
                                border.color: "#1e2430"
                                RowLayout {
                                    anchors.fill: parent
                                    anchors.margins: 20
                                    Text { text: "📄"; font.pixelSize: 32 }
                                    Item { width: 10 }
                                    ColumnLayout {
                                        Text { text: "Scan Specific File"; color: "white"; font.bold: true; font.pixelSize: 18 }
                                        Text { text: "Select a single suspicious file or executable to scan it instantly."; color: "#8e99ab" }
                                    }
                                    Item { Layout.fillWidth: true }
                                    Button {
                                        text: "Select File"
                                        Layout.preferredWidth: 120
                                        height: 40
                                        background: Rectangle { color: "#2a3441"; radius: 6 }
                                        contentItem: Text { text: parent.text; color: "white"; font.bold: true; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                                        onClicked: fileDialog.open()
                                    }
                                }
                            }
                        }
                        
                        Item { Layout.fillHeight: true }
                    }
                    
                    // 2b: Logs View
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 30
                        
                        RowLayout {
                            Layout.fillWidth: true
                            Button {
                                text: "← Back"
                                Layout.preferredWidth: 80
                                height: 35
                                background: Rectangle { color: "#2a3441"; radius: 5 }
                                contentItem: Text { text: parent.text; color: "white"; font.bold: true; horizontalAlignment: Text.AlignHCenter }
                                onClicked: scanPageContainer.innerIndex = 0
                            }
                            Item { width: 20 }
                            Text { text: "Scan Logs"; color: "white"; font.pixelSize: 24; font.bold: true; Layout.fillWidth: true }
                            Button {
                                text: "Refresh"
                                Layout.preferredWidth: 100
                                height: 35
                                background: Rectangle { color: "#1e5af6"; radius: 5 }
                                contentItem: Text { text: parent.text; color: "white"; font.bold: true; horizontalAlignment: Text.AlignHCenter }
                                onClicked: scanLogsArea.text = backend.get_threat_logs()
                            }
                        }
                        
                        Item { height: 10 }
                        
                        ScrollView {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            TextArea {
                                id: scanLogsArea
                                readOnly: true
                                text: "Loading logs..."
                                color: "#8e99ab"
                                font.family: "Courier"
                                font.pixelSize: 12
                                background: Rectangle { color: "#121824"; radius: 8; border.color: "#1e2430"; border.width: 1 }
                                padding: 15
                                wrapMode: Text.NoWrap
                            }
                        }
                    }
                }
            }

            // Page 3: Quarantine
            Rectangle {
                color: "#0a0e17"
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 30
                    Text { text: "Quarantine Box"; color: "white"; font.pixelSize: 24; font.bold: true }
                    Text { text: "Isolated malware files safely locked away."; color: "#8e99ab"; font.pixelSize: 16 }
                    
                    Item { height: 10 }
                    
                    // Table Header
                    Rectangle {
                        Layout.fillWidth: true
                        height: 40
                        color: "#121824"
                        radius: 8
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            Text { text: "Filename"; color: "white"; font.bold: true; Layout.preferredWidth: 400 }
                            Text { text: "Size"; color: "white"; font.bold: true; Layout.preferredWidth: 100 }
                            Text { text: "Quarantined Date"; color: "white"; font.bold: true; Layout.fillWidth: true }
                        }
                    }
                    
                    // Table Body
                    ListView {
                        id: quarantineList
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        spacing: 5
                        model: ListModel { id: quarantineModel }
                        delegate: Rectangle {
                            width: quarantineList.width
                            height: 45
                            color: "#0f1523"
                            radius: 8
                            border.color: "#1e2430"
                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 10
                                Text { text: model.filename; color: "#ef4444"; font.pixelSize: 14; Layout.preferredWidth: 400; elide: Text.ElideRight }
                                Text { text: model.size; color: "#8e99ab"; font.pixelSize: 14; Layout.preferredWidth: 100 }
                                Text { text: model.date; color: "#8e99ab"; font.pixelSize: 14; Layout.fillWidth: true }
                            }
                        }
                    }
                    
                    Button {
                        text: "Refresh List"
                        Layout.alignment: Qt.AlignRight
                        background: Rectangle { color: "#2a3441"; radius: 5 }
                        contentItem: Text { text: parent.text; color: "white"; font.bold: true; horizontalAlignment: Text.AlignHCenter }
                        onClicked: {
                            var files = JSON.parse(backend.get_quarantined_files())
                            quarantineModel.clear()
                            for (var i = 0; i < files.length; i++) {
                                quarantineModel.append(files[i])
                            }
                        }
                    }
                }
            }

            // Page 4: Notifications
            Rectangle {
                color: "#0a0e17"
                ColumnLayout {
                    anchors.centerIn: parent
                    Text { text: "Recent Notifications"; color: "white"; font.pixelSize: 24; font.bold: true }
                    Text { text: "System alerts will be shown here."; color: "#8e99ab"; font.pixelSize: 16 }
                }
            }

            // Page 5: Settings
            Rectangle {
                color: "#0a0e17"
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 30
                    spacing: 20
                    
                    Text { text: "Application Settings"; color: "white"; font.pixelSize: 24; font.bold: true }
                    
                    Rectangle {
                        Layout.fillWidth: true
                        height: 80
                        color: "#121824"
                        radius: 8
                        border.color: "#1e2430"
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 20
                            ColumnLayout {
                                Text { text: "Clear Threat Logs"; color: "white"; font.bold: true }
                                Text { text: "Permanently delete the scan history and reset dashboard counts."; color: "#8e99ab" }
                            }
                            Item { Layout.fillWidth: true }
                            Button {
                                text: "Clear Logs"
                                background: Rectangle { color: "#ef4444"; radius: 5 }
                                contentItem: Text { text: parent.text; color: "white"; font.bold: true; horizontalAlignment: Text.AlignHCenter }
                                onClicked: {
                                    backend.clear_threat_logs()
                                    scanLogsArea.text = backend.get_threat_logs()
                                }
                            }
                        }
                    }
                    Item { Layout.fillHeight: true }
                }
            }

            // Page 6: About
            Rectangle {
                color: "#0a0e17"
                ColumnLayout {
                    anchors.centerIn: parent
                    Text { text: "About Secure Drive"; color: "white"; font.pixelSize: 24; font.bold: true }
                    Text { text: "Version 1.0. Developed securely."; color: "#8e99ab"; font.pixelSize: 16 }
                }
            }
        }
    }
}
