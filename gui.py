import os
import threading
import tkinter as tk
from os import listdir
from os.path import isfile, join
from tkinter import filedialog, messagebox

import cv2
import sounddevice
import vlc
from PIL import Image, ImageTk

import sound_recording
import video_recording
import sound_recording_stream
import video_recording_stream

PATH = os.path.dirname(__file__) + r"\\media\\"
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
    arr.append((index, " Stream (URL needed)"))
    return arr


def init_main_window():
    def __get_ask_open_file():
        file = filedialog.askopenfile()
        print(file)
        __play_file(file.name)

    def __fill_lst_box_files():
        lst_box_files.delete(0, 'end')
        files = [f for f in listdir(PATH) if isfile(join(PATH, f)) and f[-4:] in FILE_FORMATS]
        print(*files)
        for f in files:
            lst_box_files.insert(tk.END, f)

    def __audio_record():
        try:
            # if last option choosed -> Stream
            print(int(chosen_audio_input_device.get()[1]) )
            print(audio_input_devices[-1])
            if int(chosen_audio_input_device.get()[1]) == audio_input_devices[-1][0]:
                sound_recording_stream.prepare_rec(url=entry_for_url.get(), filename=entry_for_name.get())
            else:
                sound_recording.prepare_rec(int(chosen_audio_input_device.get()[1]), entry_for_name.get())
        except:
            messagebox.showerror(title="Critical error",
                                 message="Critical error - no recording started. Please try again.")
        else:
            btn_audio_record.config(image=icon_rec, state='disabled')

    def __video_record():
        # if stream, make button not grey
        # EXCEPTIONHANDLING FALLS URL FALSCH IST!!!!
        stream = False
        try:
            # if last option choosed -> Stream
            if int(chosen_video_input_device.get()[1]) == video_input_devices[-1][0]:
                video_recording_stream.prepare_rec(url=entry_for_url.get(), filename=entry_for_name.get())
                stream = True
            else:
                video_recording.prepare_rec(int(chosen_video_input_device.get()[1]), entry_for_name.get())
        except:
            messagebox.showerror(title="Critical error",
                                 message="Critical error - no recording started. Please try again.")
        else:
            if not stream:
                btn_video_record.config(image=icon_rec, state='disabled')

    def __play_file(file=None):
        print('playing file')
        try:
            if not file:
                file = PATH + lst_box_files.get(lst_box_files.curselection()[0])
        except IndexError:
            messagebox.showwarning(title="Nothing to play", message="Please chose a file from list")
        else:
            new_media = instance.media_new(file)
            player.set_media(new_media)
            t = threading.Thread(target=player.play)
            t.start()

    def __play_pause():
        print(player.is_playing())
        if player.is_playing():
            player.set_pause(1)
        else:
            player.set_pause(0)

    def __stop_all():
        player.stop()
        sound_recording.stop_rec()
        video_recording.stop_rec()
        entry_for_name.delete(0, 'end')
        btn_audio_record.config(image=icon_mic, state='active')
        btn_video_record.config(image=icon_cam, state='active')
        __fill_lst_box_files()

    def __delete_selected():
        try:
            file = PATH + lst_box_files.get(lst_box_files.curselection()[0])
        except IndexError:
            messagebox.showwarning(title="Nothing to delete", message="Please select a file! ")
        else:
            if messagebox.askyesno(title="Delete File?", message=f"Are you sure you want to delete {file}?"):
                try:
                    os.remove(file)
                except OSError as error:
                    messagebox.showerror(title="Not possible",
                                         message=f"There was a system error, while deleting! {error}")
                else:
                    messagebox.showinfo(title="Deleted successful", message="File deleted!")
                __fill_lst_box_files()

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
    btn_folder = tk.Button(master=frm_top, image=icon_folder, width='20px', height='20px',
                           command=__get_ask_open_file)
    btn_folder.pack(side=tk.LEFT, padx=2)

    # get input device options
    audio_input_devices = [(sounddevice.query_devices().index(device), device.get('name'),)
                           for device in sounddevice.query_devices()
                           if device.get('max_input_channels') > 0]
    audio_input_devices.append((audio_input_devices[-1][0] + 1, "Stream (URL needed)"))
    video_input_devices = __get_video_devices()

    chosen_audio_input_device = tk.StringVar(frm_top)
    chosen_video_input_device = tk.StringVar(frm_top)

    chosen_audio_input_device.set(audio_input_devices[0].__str__())
    chosen_video_input_device.set(video_input_devices[0])

    drop_audio_input_devices = tk.OptionMenu(frm_top, chosen_audio_input_device, *audio_input_devices)
    drop_audio_input_devices.config(width=75)
    lbl_audio_input_devices = tk.Label(master=frm_top, text="Select video device")
    drop_video_input_devices = tk.OptionMenu(frm_top, chosen_video_input_device, *video_input_devices)
    drop_video_input_devices.config(width=40)
    lbl_video_input_devices = tk.Label(master=frm_top, text="Select audio device")

    drop_audio_input_devices.pack(side=tk.RIGHT)
    lbl_audio_input_devices.pack(side=tk.RIGHT)
    drop_video_input_devices.pack(side=tk.RIGHT)
    lbl_video_input_devices.pack(side=tk.RIGHT)

    # file list section
    frm_list = tk.Frame(master=window, width=400, height=700)  # , bg="White", borderwidth=1)
    lst_box_files = tk.Listbox(master=frm_list, width=23)
    __fill_lst_box_files()
    lst_box_files.pack(anchor="w")
    frm_list.pack(anchor="w")
    btn_remove = tk.Button(master=frm_list, text="delete",
                           command=__delete_selected)
    btn_remove.pack(pady=4)
    tk.Label(master=frm_list, text="Filename for Recording:").pack(anchor="w")
    entry_for_name = tk.Entry(master=frm_list, width=23)
    entry_for_name.pack(anchor="w", pady=4)
    tk.Label(master=frm_list, text="URL to source (stream):").pack(anchor="w")
    entry_for_url = tk.Entry(master=frm_list, width=23)
    entry_for_url.pack(anchor="w", pady=4)

    # video player section
    frm_video = tk.Frame(master=window, width=400, height=500)
    lbl_video = tk.Label(master=frm_video)
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new('')
    if os.name == 'nt':
        player.set_hwnd(frm_video.winfo_id())
    else:
        player.set_xwindow(frm_video.winfo_id())

    player.set_media(media)
    player.audio_set_volume(100)

    # bottom section --> under file selection
    # frm_bottom = tk.Frame(master=window, width=500, height=20)

    btn_audio_record = tk.Button(master=frm_list, image=icon_mic, command=__audio_record)
    btn_video_record = tk.Button(master=frm_list, image=icon_cam, command=__video_record)
    btn_play = tk.Button(master=frm_list, image=icon_play, command=__play_file)

    btn_pause = tk.Button(master=frm_list, image=icon_pause, command=__play_pause)
    btn_stop = tk.Button(master=frm_list, image=icon_stop, command=__stop_all)

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
    # frm_bottom.pack(side=tk.BOTTOM)

    window.mainloop()


if __name__ == "__main__":
    init_main_window()