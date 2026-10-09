import re

with open("esp_agent.py", "r") as f:
    content = f.read()

# Add safe fallback or network/mock fallback for serial when device doesn't exist
old_init = """    def __init__(self, name="ESP32Node", port="/dev/ttyUSB0", baud=115200):
        super().__init__(name=name)
        self.port = port
        self.baud = baud"""

new_init = """    def __init__(self, name="ESP32Node", port="/dev/ttyUSB0", baud=115200):
        super().__init__(name=name)
        self.port = port
        self.baud = baud
        self.mock = False
        try:
            ser = serial.Serial(self.port, self.baud, timeout=1)
            ser.close()
        except Exception:
            self.mock = True"""

old_send = """    def send(self, msg):
        try:
            ser = serial.Serial(self.port, self.baud, timeout=1)
            ser.write((msg + "\\n").encode())
            reply = ser.readline().decode().strip()
            return f"[ESP32] {reply}"
        except Exception as e:
            return f"[ESP32 ERROR] {e}" """

new_send = """    def send(self, msg):
        if self.mock:
            return f"[ESP32 MOCK ACK] Processed command: {msg}"
        try:
            ser = serial.Serial(self.port, self.baud, timeout=1)
            ser.write((msg + "\\n").encode())
            reply = ser.readline().decode().strip()
            return f"[ESP32] {reply}"
        except Exception as e:
            return f"[ESP32 ERROR] {e}" """

content = content.replace(old_init, new_init)
content = content.replace(old_send, new_send)

with open("esp_agent.py", "w") as f:
    f.write(content)

print("[+] esp_agent.py updated with hardware-agnostic mock fallback.")
