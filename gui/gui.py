import tkinter as tk
import tkinter.filedialog as files

import vlc
from PIL import Image, ImageTk
from PIL.Image import Resampling


def init_main_window():
    window = tk.Tk()
    window.title('Tkinter Multimedia Player')

    # window.tk.call("source", "assets/azure.tcl")
    # window.tk.call("set_theme", "dark")

    # file actions
    # files.asksaveasfilename()
    # files.asksaveasfile()
    # files.askopenfilename()
    # files.askopenfile()
    # files.askdirectory()
    # files.askopenfilenames()
    # files.askopenfiles()

    # icons
    icon_play = Image.open('assets/images/icons/play-button.png').resize((20, 20), Resampling.LANCZOS)
    icon_pause = Image.open('assets/images/icons/pause-button.png').resize((20, 20), Resampling.LANCZOS)
    icon_stop = Image.open('assets/images/icons/stop-button.png').resize((20, 20), Resampling.LANCZOS)
    icon_folder = Image.open('assets/images/icons/folder.png').resize((20, 20), Resampling.LANCZOS)
    icon_mic = Image.open('assets/images/icons/microphone.png').resize((20, 20), Resampling.LANCZOS)
    icon_play = ImageTk.PhotoImage(icon_play)
    icon_pause = ImageTk.PhotoImage(icon_pause)
    icon_stop = ImageTk.PhotoImage(icon_stop)
    icon_folder = ImageTk.PhotoImage(icon_folder)
    icon_mic = ImageTk.PhotoImage(icon_mic)

    # top menu  section
    frm_top = tk.Frame(master=window, width=500, height=20)
    btn_folder = tk.Button(master=frm_top, image=icon_folder, width='20px', height='20px', command=files.askopenfile)
    btn_folder.pack(side=tk.LEFT, padx=2)

    # file list section
    frm_list = tk.Frame(master=window, width=300, height=500, bg="White", borderwidth=1)

    # video player section
    frm_video = tk.Frame(master=window, width=500, height=500)

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new('assets/Dateiname.avi')
    player.set_xwindow(frm_video.winfo_id())
    player.set_media(media)
    player.audio_set_volume(100)

    # bottom section
    # TODO: indicators for recording, vidoe/audio state
    frm_bottom = tk.Frame(master=window, width=500, height=20)

    # TODO: video and sound record seperatly
    btn_record = tk.Button(master=frm_bottom, image=icon_mic, command='')
    btn_play = tk.Button(master=frm_bottom, image=icon_play, command=player.play)
    btn_pause = tk.Button(master=frm_bottom, image=icon_pause, command=lambda: player.set_pause(1))
    btn_stop = tk.Button(master=frm_bottom, image=icon_stop, command=player)
    btn_record.pack(side=tk.LEFT, padx=2)
    btn_play.pack(side=tk.LEFT, padx=2)
    btn_pause.pack(side=tk.LEFT, padx=2)
    btn_stop.pack(side=tk.LEFT, padx=2)
    btn_record.pack(side=tk.LEFT, padx=2)

    # packing frames
    frm_top.pack(side=tk.TOP)
    frm_list.pack(side=tk.LEFT)
    frm_video.pack(side=tk.RIGHT, anchor=tk.S, expand=tk.YES, fill=tk.BOTH)
    frm_bottom.pack(side=tk.BOTTOM)

    window.mainloop()


if __name__ == "__main__":
    init_main_window()
