import serial

from src.Dummy import DummySerial
class Mbed_Connection:
    def __init__(self, use_dummy=False):
        self.use_dummy = use_dummy
        self.ser = None

    def open(self, port, baudrate=9600, timeout=1):
        if self.use_dummy:
                self.ser = DummySerial(port, baudrate, timeout=timeout)
                print('using dummy')
        else:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=timeout)
                print(f"Serial port {port} opened at {baudrate} baud.")
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
                self.ser = None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed.")

    def is_open(self):
        return self.ser is not None and self.ser.is_open

    def write_string(self, message):
        if self.is_open():
            try:
                bytes_written = self.ser.write(message.encode('utf-8'))
                print(f"Sent {bytes_written} bytes: {message}")
            except serial.SerialException as e:
                print(f"Error writing to serial port: {e}")
        else:
            print("Serial port is not open. Cannot send data.")


