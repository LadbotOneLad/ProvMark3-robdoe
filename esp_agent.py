from crewai import OperatorAgent
import serial

class ESP32Agent(OperatorAgent):
    def __init__(self, name="ESP32Node", port="/dev/ttyUSB0", baud=115200):
        super().__init__(name=name)
        self.port = port
        self.baud = baud
        self.mock = True

    def send(self, msg):
        if self.mock:
            return f"[ESP32 MOCK ACK] Processed command: {msg}"
        try:
            ser = serial.Serial(self.port, self.baud, timeout=1)
            ser.write((msg + "\n").encode())
            reply = ser.readline().decode().strip()
            return f"[ESP32] {reply}"
        except Exception as e:
            return f"[ESP32 ERROR] {e}"

    def run(self, input_text):
        text = input_text.upper()

        # direct ESP32 commands
        if text.startswith("ESP:"):
            cmd = input_text.split("ESP:", 1)[1].strip()
            return self.send(cmd)

        # identity triggers routed through ESP32
        if "GENESIS" in text:
            return self.send("GENESIS")

        if "ATOM" in text:
            return self.send("ATOM")

        if "TRUTH" in text:
            return self.send("TRUTH")

        # fallback to OperatorAgent logic
        return super().run(input_text)


# ----------------------------------------------------
# LIVE MODE — RUN DIRECTLY
# ----------------------------------------------------
if __name__ == "__main__":
    agent = ESP32Agent()

    print(">>> ESP32 LIVE MODE (MOCK FALLBACK ACTIVE)")
    print(">>> Type commands like:")
    print(">>>   ESP:ping")
    print(">>>   ESP:status")
    print(">>>   GENESIS / ATOM / TRUTH")
    print(">>> CTRL+C to exit\n")

    while True:
        try:
            cmd = input("ESP32> ")
            out = agent.run(cmd)
            print(out)
        except KeyboardInterrupt:
            print("\n>>> EXITING LIVE MODE")
            break
