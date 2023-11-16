from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QWidget, QStatusBar, QTabWidget, QComboBox,
                             QGridLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPointF
import sys
import serial.tools.list_ports


class MavlinkInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        # Central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Tab widget for different sections
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # Connection tab
        self.connection_tab = QWidget()
        self.tabs.addTab(self.connection_tab, "Connection")

        # Map tab
        self.map_tab = QWidget()
        self.tabs.addTab(self.map_tab, "Map")
        # Initialize the map tab with offline map
        self.init_map_tab()

        # Connection tab layout
        self.connection_layout = QGridLayout(self.connection_tab)

        # Map tab layout
        self.map_layout = QVBoxLayout(self.map_tab)
        self.map_label = QLabel("Map Display Placeholder")
        self.map_layout.addWidget(self.map_label)
        # Future map integration would go here

        # Master connection widgets
        self.master_label = QLabel("Master COM Port:")
        self.master_com_input = QComboBox()
        self.master_com_input.addItems(self.get_serial_ports())
        self.master_baud_rate = QComboBox()
        self.master_baud_rate.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.master_connect_button = QPushButton("Connect")
        self.master_connect_button.clicked.connect(self.connect_master)

        # Rover connection widgets
        self.rover_label = QLabel("Rover COM Port:")
        self.rover_com_input = QComboBox()
        self.rover_com_input.addItems(self.get_serial_ports())
        self.rover_baud_rate = QComboBox()
        self.rover_baud_rate.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.rover_connect_button = QPushButton("Connect")
        self.rover_connect_button.clicked.connect(self.connect_rover)

        # Populate connection tab layout
        self.connection_layout.addWidget(self.master_label, 0, 0)
        self.connection_layout.addWidget(self.master_com_input, 0, 1)
        self.connection_layout.addWidget(self.master_baud_rate, 0, 2)
        self.connection_layout.addWidget(self.master_connect_button, 0, 3)
        self.connection_layout.addWidget(self.rover_label, 1, 0)
        self.connection_layout.addWidget(self.rover_com_input, 1, 1)
        self.connection_layout.addWidget(self.rover_baud_rate, 1, 2)
        self.connection_layout.addWidget(self.rover_connect_button, 1, 3)

        # Status bar for connection status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Disconnected")

        # Set window title and size
        self.setWindowTitle("MAVLink Interface")
        self.setGeometry(100, 100, 800, 200)

    def init_map_tab(self):
        # Create the QGraphicsScene and QGraphicsView for displaying the map
        self.map_scene = QGraphicsScene()
        self.map_view = QGraphicsView(self.map_scene, self.map_tab)

        # Load the offline map image and add it to the scene
        self.map_pixmap = QPixmap('path_to_your_offline_map_image.png')  # Replace with your offline map image path
        self.map_item = QGraphicsPixmapItem(self.map_pixmap)
        self.map_scene.addItem(self.map_item)

        # Load the marker image and add it to the scene
        self.marker_pixmap = QPixmap('path_to_your_marker_image.png')  # Replace with your marker image path
        self.marker_item = QGraphicsPixmapItem(self.marker_pixmap)

        # Load the marker image and add it to the scene
        self.marker_pixmap = QPixmap('path_to_your_marker_image.png')  # Replace with your marker image path
        self.marker_item = QGraphicsPixmapItem(self.marker_pixmap)

        # Set the position for Taipei 101 on the map
        # Replace these with the actual pixel coordinates on your map image where Taipei 101 is located
        x_coordinate = 300  # Example x coordinate
        y_coordinate = 400  # Example y coordinate
        self.taipei_101_position = QPointF(x_coordinate, y_coordinate)
        self.marker_item.setPos(self.taipei_101_position)

        # Set the position for Taipei 101 on the map
        # These should be the pixel coordinates on your map image where Taipei 101 is located
        self.taipei_101_position = QPointF(x_coordinate, y_coordinate)  # Replace with actual coordinates
        self.marker_item.setPos(self.taipei_101_position)

        # Add the marker to the scene
        self.map_scene.addItem(self.marker_item)

        # Set the scene to the QGraphicsView
        self.map_view.setScene(self.map_scene)

        # Add the QGraphicsView to the map tab layout
        self.map_layout.addWidget(self.map_view)

    def get_serial_ports(self):
        # Lists serial port names
        port_list = serial.tools.list_ports.comports()
        ports = [port.device for port in port_list]
        return ports

    def connect_master(self):
        # Implement master connection logic here
        pass

    def connect_rover(self):
        # Implement rover connection logic here
        pass

def main():
    app = QApplication(sys.argv)
    mavlink_interface = MavlinkInterface()
    mavlink_interface.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
