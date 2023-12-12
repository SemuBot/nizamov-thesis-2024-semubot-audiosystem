from tuning import Tuning
import usb.core
import usb.util
import time

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

voice_array = []

if dev:
    Mic_tuning = Tuning(dev)
    print (Mic_tuning.is_voice())
    while True:
        try:
            voice_array.append(Mic_tuning.is_voice())
            print (Mic_tuning.is_voice())
            time.sleep(0.2)
        except KeyboardInterrupt:
            break