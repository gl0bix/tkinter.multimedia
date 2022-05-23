import datetime
import requests
import threading

global finished


def record(url, filename):
    file = open(filename, 'wb')
    chunk_size = 1024

    with requests.Session() as s:
        response = s.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                file.write(chunk)
        file.close()
    global finished
    finished = True


# example URL: "https://static-eus-rs.wondershare.com/Filmstock/file/s5/7a184ee5c5152b6f246640655570ec4e.mp4"
def prepare_rec(url, filename=None):
    if not url:
        raise Exception("No URL given!")
    if not filename:
        filename = "unnamed_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + ".mp4"
    if filename.strip()[-3:] != "mp4":
        filename = filename.strip() + ".mp4"
    filename = "../gui/assets/recordings/" + filename
    threading.Thread(target=record, args=(url, filename,)).start()