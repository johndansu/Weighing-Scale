import serial
import time

def read_from_serial(port='/dev/ttyUSB0', baudrate=9600):
    try:
        # Open the serial port
        with serial.Serial(port, baudrate, timeout=1) as ser:
            time.sleep(2)  # Allow some time for the connection to establish
            line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
            return line
    except Exception as e:
        print(f"Error reading from serial port: {e}")
        return None
