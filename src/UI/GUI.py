import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QComboBox, QInputDialog 
)
import serial.tools.list_ports

from src.Mbed import Mbed_Connection
from src.UI.inputWidgets import InputsWidget
from src.Log import Logger


class MainWindow(QMainWindow):

    def __init__(self, user_id):
        super().__init__()
        self.logger = Logger(user_id)
        self.user_id = user_id
        self.setWindowTitle(f"User ID: {self.user_id}")
        self.sent_inputs = False
        self.stored_max = None
        self.stored_min = None
        self.calibration_counter = 0 

        self.stored_med_cal_min = None
        self.stored_med_cal_max = None

        self.serial_connection = Mbed_Connection(use_dummy=True)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget) # why is this not self
        self.layout.setSpacing(15)

        self.port_combo = QComboBox()
        self.refresh_ports()
        self.layout.addWidget(QLabel("Select Serial Port:"))
        self.layout.addWidget(self.port_combo)

        # Inputs layout
        self.inputs_widget = InputsWidget()
        self.layout.addWidget(self.inputs_widget)

        # Connect / Disconnect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.handle_connect)
        self.layout.addWidget(self.connect_button)

        # Send data button
        self.send_button = QPushButton("Send Inputs")
        self.send_button.clicked.connect(self.send_inputs)
        self.send_button.setEnabled(False) 
        self.layout.addWidget(self.send_button)

        # Max and min Buttons 
        max_min_layout = QHBoxLayout()
        self.layout.addLayout(max_min_layout)

        self.store_max_button = QPushButton("Store Max")
        self.store_max_button.clicked.connect(self.store_max)
        self.store_max_button.setEnabled(False) 
        max_min_layout.addWidget(self.store_max_button)

        self.send_prev_max_button = QPushButton("Send Previous Max")
        self.send_prev_max_button.clicked.connect(self.send_prev_max)
        self.send_prev_max_button.setEnabled(False) 
        max_min_layout.addWidget(self.send_prev_max_button)

        # Min buttons
        self.store_min_button = QPushButton("Store Min")
        self.store_min_button.clicked.connect(self.store_min)
        self.store_min_button.setEnabled(False)
        max_min_layout.addWidget(self.store_min_button)

        self.send_prev_min_button = QPushButton("Send Previous Min")
        self.send_prev_min_button.clicked.connect(self.send_prev_min)
        self.send_prev_min_button.setEnabled(False) 
        max_min_layout.addWidget(self.send_prev_min_button)

        # Upate calibration session 
        self.update_calibration_button = QPushButton(f'Update calibration, current count: {self.calibration_counter}')
        self.update_calibration_button.clicked.connect(self.update_calibration)
        self.layout.addWidget(self.update_calibration_button)


        # calibration saves layout 
        calibration_layout = QHBoxLayout()
        self.layout.addLayout(calibration_layout)

        self.stored_med_cal_min_button = QPushButton("Store Meditation Calibration Min")

        # Text area to show output
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.layout.addWidget(self.text_area)

        self.setCentralWidget(self.widget)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        if ports:
            for port in ports:
                self.port_combo.addItem(port.device)
        else:
            self.port_combo.addItem("Dummy")

    def handle_connect(self):
        if not self.serial_connection.is_open():
            selected_port = self.port_combo.currentText()
            if not selected_port:
                self.text_area.append("No serial port selected.")
                return
            self.serial_connection.open(port=selected_port, baudrate=9600)
            if self.serial_connection.is_open():
                self.send_button.setEnabled(True)
                self.connect_button.setText("Disconnect")
            else:
                self.text_area.append("Failed to open serial port.")
        else:
            self.serial_connection.close()
            self.send_button.setEnabled(False)
            self.connect_button.setText("Connect")

    def send_inputs(self):
        final_string = self.inputs_widget.collect_inputs_as_string()
        self.serial_connection.write_string(final_string+"\n")
        self.text_area.append(f"Sent: {final_string}")
        self.logger.write_raw(final_string, self.calibration_counter)
        self.sent_inputs = True
        self.store_max_button.setEnabled(True)
        self.store_min_button.setEnabled(True)

    def store_max(self):
        if self.sent_inputs:
            self.stored_max = self.inputs_widget.collect_inputs_as_string()
            self.logger.write_calibration(self.stored_max, self.calibration_counter)
            self.send_prev_max_button.setEnabled(True)
        else:
            self.text_area.append("Error: No inputs have been sent yet!")

    def send_prev_max(self):
        if self.stored_max:
            self.serial_connection.write_string(self.stored_max + "\n")
            self.text_area.append(f"Sent Previous Max: {self.stored_max}")
        else:
            self.text_area.append("No max value stored yet.")

    def store_min(self):
        if self.sent_inputs:
            self.stored_min = self.inputs_widget.collect_inputs_as_string()
            self.logger.write_calibration(self.stored_max, self.calibration_counter)
            self.send_prev_min_button.setEnabled(True)
        else:
            self.text_area.append("Error: No inputs have been sent yet!")

    def send_prev_min(self):
        if self.stored_min:
            self.serial_connection.write_string(self.stored_min + "\n")
            self.text_area.append(f"Sent Previous Max: {self.stored_min}")
        else:
            self.text_area.append("No min value stored yet.")

    def closeEvent(self, event):
        self.serial_connection.close()
        event.accept()


    def update_calibration(self):
        self.calibration_counter +=1
        self.update_calibration_button.setText(f'Update calibration, current count: {self.calibration_counter}')

