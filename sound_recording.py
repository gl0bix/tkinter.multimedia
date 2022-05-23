import datetime
import queue
import threading

import numpy
import sounddevice
import soundfile

assert numpy

stop = False


def start_recording(filename, device_id, sample_rate):
    global stop
    stop = False
    q = queue.Queue()

    # Function to Copy audio_block from InputStream into Queue
    def callback(audio_block, frames, time, status):
        q.put(audio_block.copy())

    # create new soundfile
    with soundfile.SoundFile(filename, mode='w', samplerate=sample_rate, channels=2) as file:
        # Start InputStream (Callback = called periodically with recorded Data)
        with sounddevice.InputStream(samplerate=sample_rate, channels=2, device=device_id, callback=callback):
            # check if new element in Queue and write it in File
            while True:
                file.write(q.get())
                if stop:
                    break


def prepare_rec(device_id=1, filename=None):
    if not filename:
        filename = "./media/rec_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".wav"
    if filename.strip()[-3:] != "wav":
        filename = filename.strip() + ".wav"
    samplerate = sounddevice.query_devices()[device_id]["default_samplerate"]
    threading.Thread(target=start_recording, args=(filename, device_id, int(samplerate))).start()


def stop_rec():
    global stop
    stop = True


