import os
import threading
import tkinter as tk
from os import listdir
from os.path import isfile, join
from tkinter import filedialog

import cv2
import sounddevice
import vlc
from PIL import Image, ImageTk

import sound_recording
import video_recording

PATH = os.path.dirname(__file__)
FILE_FORMATS = ('.avi', '.mp4', 'mp3', '.wav')

# solution from: https://stackoverflow.com/questions/8044539/listing-available-devices-in-python-opencv
def __get_video_devices():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append((index, cap.getBackendName()))
        index += 1
    return arr


def init_main_window():

    def __play_file(file):
        print('playing file')
        new_media = instance.media_new(file)
        player.set_media(new_media)
        t = threading.Thread(target=player.play)
        t.start()

    window = tk.Tk()
    window.title('Tkinter Multimedia Player')

    # file actions
    # files.asksaveasfilename()
    # files.asksaveasfile()
    # files.askopenfilename()
    # files.askopenfile()
    # files.askdirectory()
    # files.askopenfilenames()
    # files.askopenfiles()

    # icons
    icon_play = Image.open('assets/images/icons/play-button.png').resize((20, 20))
    icon_pause = Image.open('assets/images/icons/pause-button.png').resize((20, 20))
    icon_stop = Image.open('assets/images/icons/stop-button.png').resize((20, 20))
    icon_folder = Image.open('assets/images/icons/folder.png').resize((20, 20))
    icon_mic = Image.open('assets/images/icons/microphone.png').resize((20, 20))
    icon_cam = Image.open('assets/images/icons/video-camera.png').resize((20, 20))
    icon_rec = Image.open('assets/images/icons/icon_record.png').resize((20, 20))
    icon_play = ImageTk.PhotoImage(icon_play)
    icon_pause = ImageTk.PhotoImage(icon_pause)
    icon_stop = ImageTk.PhotoImage(icon_stop)
    icon_folder = ImageTk.PhotoImage(icon_folder)
    icon_mic = ImageTk.PhotoImage(icon_mic)
    icon_cam = ImageTk.PhotoImage(icon_cam)
    icon_rec = ImageTk.PhotoImage(icon_rec)

    # top menu  section
    frm_top = tk.Frame(master=window, width=500, height=20)
    btn_folder = tk.Button(master=frm_top, image=icon_folder, width='20px', height='20px', command=filedialog.askopenfile)
    btn_folder.pack(side=tk.LEFT, padx=2)

    # get input device options
    audio_input_devices = [(sounddevice.query_devices().index(device), device.get('name'),)
                     for device in sounddevice.query_devices()
                     if device.get('max_input_channels') > 0]
    video_input_devices = __get_video_devices()

    chosen_audio_input_device = tk.StringVar(frm_top)
    chosen_video_input_device = tk.StringVar(frm_top)

    chosen_audio_input_device.set(audio_input_devices[0])
    chosen_video_input_device.set(video_input_devices[0])

    drop_audio_input_devices = tk.OptionMenu(frm_top, chosen_audio_input_device, *audio_input_devices)
    lbl_audio_input_devices = tk.Label(master=frm_top, text="Select input device")
    drop_video_input_devices = tk.OptionMenu(frm_top, chosen_video_input_device, *video_input_devices)
    lbl_video_input_devices = tk.Label(master=frm_top, text="Select output device")

    drop_audio_input_devices.pack(side=tk.RIGHT)
    lbl_audio_input_devices.pack(side=tk.RIGHT)
    drop_video_input_devices.pack(side=tk.RIGHT)
    lbl_video_input_devices.pack(side=tk.RIGHT)

    # file list section
    frm_list = tk.Frame(master=window, width=300, height=500, bg="White", borderwidth=1)

    files = [f for f in listdir(PATH) if isfile(join(PATH, f)) and f[-4:] in FILE_FORMATS]
    print(*files)
    lst_box_files = tk.Listbox(master=frm_list)
    lst_box_files.pack()
    for f in files:
        lst_box_files.insert(tk.END, f)
    frm_list.pack()

    # video player section
    frm_video = tk.Frame(master=window, width=500, height=500)
    lbl_video = tk.Label(master=frm_video)
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new('')
    player.set_xwindow(frm_video.winfo_id())
    player.set_media(media)
    player.audio_set_volume(100)

    # bottom section
    frm_bottom = tk.Frame(master=window, width=500, height=20)

    btn_audio_record = tk.Button(master=frm_bottom, image=icon_mic,
                                 command=lambda: [sound_recording.prepare_rec(int(chosen_audio_input_device.get()[1]), 'record_from_chosen_device'),
                                                  btn_audio_record.config(image=icon_rec, state='disabled')])
    btn_video_record = tk.Button(master=frm_bottom, image=icon_cam,
                                 command=lambda: [video_recording.prepare_rec(int(chosen_video_input_device.get()[1]), 'video_filename'),
                                                  btn_video_record.config(image=icon_rec, state='disabled')])
    btn_play = tk.Button(master=frm_bottom, image=icon_play,
                         command=lambda: __play_file(lst_box_files.get(lst_box_files.curselection()[0])))
    btn_pause = tk.Button(master=frm_bottom, image=icon_pause, command=lambda: player.set_pause(1))
    btn_stop = tk.Button(master=frm_bottom, image=icon_stop, command='')
    btn_audio_record.pack(side=tk.LEFT, padx=2)
    btn_video_record.pack(side=tk.LEFT, padx=2)
    btn_play.pack(side=tk.LEFT, padx=2)
    btn_pause.pack(side=tk.LEFT, padx=2)
    btn_stop.pack(side=tk.LEFT, padx=2)
    btn_audio_record.pack(side=tk.LEFT, padx=2)

    # packing frames
    frm_top.pack(side=tk.TOP)
    frm_list.pack(side=tk.LEFT)
    frm_video.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
    frm_bottom.pack(side=tk.BOTTOM)

    window.mainloop()


if __name__ == "__main__":
    init_main_window()
