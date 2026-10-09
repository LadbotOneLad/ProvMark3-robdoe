import usb.core
import usb.util
from crewai import OperatorAgent

class ESP32RawAgent(OperatorAgent):
    def __init__(self, name="ESP32RawNode", vid=0x303A, pid=0x1001):
        super().__init__(name=name)
        self.dev = usb.core.find(idVendor=vid, idProduct=pid)
        if self.dev is None:
            raise ValueError("Myware device not found")

        try:
            self.dev.set_configuration()
        except:
            pass

    def send(self, msg):
        try:
            data = msg.encode()
            self.dev.write(1, data)  # endpoint 1 OUT
            reply = self.dev.read(0x81, 64)  # endpoint 0x81 IN
            return f"[MYWARE] {bytes(reply).decode(errors='ignore')}"
        except Exception as e:
            return f"[MYWARE ERROR] {e}"

    def run(self, input_text):
        return self.send(input_text)
