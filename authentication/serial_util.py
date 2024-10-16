import serial

def read_from_serial():
    try:
        # Set up the serial connection (adjust the port and baudrate as per your device)
        ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust the COM port (e.g., COM3)
        ser.flush()

        # Read data from the serial port
        if ser.in_waiting > 0:
            weight_data = ser.readline().decode('utf-8').strip()
            return weight_data
        return None  # Return None if no data is available
    except Exception as e:
        print(f"Error reading from serial: {e}")
        return None
