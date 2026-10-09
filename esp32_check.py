import serial

try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.write(b'ping\n')
    reply = ser.readline().decode().strip()
    print("ESP32 replied:", reply)
except Exception as e:
    print("ESP32 not responding:", e)
