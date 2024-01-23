from tuning import Tuning
import usb.core
import usb.util
import time
import os
from multiprocessing import Process, Queue

def audio_direction_worker(queue):
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

    if not dev:
        print("USB device not found.")
        return

    Mic_tuning = Tuning(dev)
    print(Mic_tuning.direction)

    while not os.path.exists("recording_done.txt"):
        try:
            angle_value = Mic_tuning.direction
            queue.put(angle_value)
            print(angle_value)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    # Create a Queue for interprocess communication
    queue = Queue()

    # Start the audio direction worker process
    audio_direction_process = Process(target=audio_direction_worker, args=(queue,))
    audio_direction_process.start()

    # Wait for the process to finish
    audio_direction_process.join()
