import subprocess
import time
import os

try:
    print("Preparing for recording...")
    time.sleep(1.5)
    record_process = subprocess.Popen(['python', 'record.py'])

    time.sleep(2.7)

    doa_process = subprocess.Popen(['python', 'doa.py'])

    # Wait for both processes to finish
    record_process.wait()
    doa_process.wait()
except KeyboardInterrupt:
    print("Process was abrupted")

os.remove("recording_done.txt")

#for doa into ipynb for graphs record mean and std dev for each array of doa data and put it against the x = 1,2,3,4 meters (in estonian)
#Then compare the error rate for some estonian sentence to the reference of it
