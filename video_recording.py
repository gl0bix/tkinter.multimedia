import datetime
import os
import threading
import tkinter

import cv2


def start_recording(filename, device_id):
    cap = cv2.VideoCapture(device_id)
    cap.set(3, 1280)
    cap.set(4, 720)
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 25, (1280, 720))
    while not stop:
        ret, frame = cap.read()
        out.write(frame)
        b = cv2.resize(frame, (640, 360), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        cv2.imshow('frame', b)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def prepare_rec(device_id=0, filename=None):
    if not filename:
        filename = "unnamed_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".avi"
    if filename.strip()[-3:] != "avi":
        filename = filename.strip() + ".avi"
    threading.Thread(target=start_recording, args=(filename, device_id,)).start()


def stop_rec():
    global stop
    stop = True
    root.destroy()


def get_av_cams():
    # Ablauf zum Bestimmen angeschlossener
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        try:
            if cap.getBackendName() == "MSMF":
                arr.append(index)
        except:
            pass
        cap.release()
        index += 1
        i -= 1
    print(arr)


if __name__ == "__main__":
    stop = False
    root = tkinter.Tk()
    tkinter.Button(root, text="Start",
                   command=lambda: prepare_rec(filename="Dateiname.avi", device_id=0)).pack()
    tkinter.Button(root, text="Stop", command=stop_rec).pack()

    get_av_cams()
    root.mainloop()
