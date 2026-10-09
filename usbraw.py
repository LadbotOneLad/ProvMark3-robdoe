import os, sys

# termux-usb passes the *file descriptor* as argv[1]
fd = int(sys.argv[1])
f = os.fdopen(fd, 'rb+', buffering=0)

print("USB FD:", fd)

while True:
    data = f.read(64)
    if not data:
        break
    print("RX:", data)
