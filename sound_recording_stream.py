import threading
from datetime import datetime
from urllib import request

global stop


def record(url, filename):
    global stop
    stop = False
    bs = 100
    stream = request.urlopen(url)  # http://fritz.de/livemp3
    with open(filename, 'wb') as f:
        while not stop:
            f.write(stream.read(bs))


# example for URL_ ="http://fritz.de/livemp3"
def prepare_rec(url, filename=None):
    request.urlopen(url)
    if not filename:
        filename = "str_" + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".mp3"
    if filename.strip()[-3:] != "mp3":
        filename = filename.strip() + ".mp3"
    filename = "../gui/assets/recordings/" + filename
    threading.Thread(target=record, args=(url, filename,)).start()


def stop_rec():
    global stop
    stop = True
