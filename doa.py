from tuning import Tuning
import usb.core
import usb.util
import time
import os

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

angle_array  = []

if dev:
    Mic_tuning = Tuning(dev)
    print (Mic_tuning.direction)
    while not os.path.exists("recording_done.txt"):
        try:
            angle_array.append(Mic_tuning.direction)
            print (Mic_tuning.direction)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
    print(angle_array, len(angle_array))
    