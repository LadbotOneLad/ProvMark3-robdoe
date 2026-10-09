import usb.core
import usb.util

print("MYWARE LIVE MODE")
print("Myware> ", end="", flush=True)

dev = usb.core.find()
if dev is None:
    print("No Myware USB device found")
    exit(1)

try:
    dev.set_configuration()
except:
    pass

ep_out = 1
ep_in = 0x81

while True:
    try:
        cmd = input()
        dev.write(ep_out, cmd.encode())
        reply = dev.read(ep_in, 64)
        print("[MYWARE]", bytes(reply).decode(errors='ignore'))
        print("Myware> ", end="", flush=True)
    except Exception as e:
        print("[MYWARE ERROR]", e)
        print("Myware> ", end="", flush=True)
