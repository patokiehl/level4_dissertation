import serial

class DummySerial:
    def __init__(self, port, baudrate=9600, timeout=1):
        print(f"Dummy serial port '{port}' opened at {baudrate} baud.")
        self._is_open = True

    def write(self, message_bytes):
        print(f"Dummy write: {message_bytes.decode('utf-8')}")
        return len(message_bytes)

    def close(self):
        print("Dummy serial port closed.")
        self._is_open = False
        
    def is_open(self):
        return self._is_open
