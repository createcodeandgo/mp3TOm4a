from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path
import shlex
import subprocess

import vlc

import view.parentview as view


class MetaView(view.View):
    '''Show file window'''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app

        self.extracted = False
        self.inserted = False

        self.d = {}

    def view(self):
        self.v = ttk.Frame(self.app.root, borderwidth=5, relief="ridge", width=600, height=600)
        self.v.grid(row=0, column=0, sticky="nswe")

        hello_label = ttk.Label(self.v, text='put chapter information into m4a')
        hello_label.grid(row=0, column=0, sticky='nesw', pady=(40, 40), padx=(60, 60))

        extract_button = ttk.Button(self.v, text='extract meta data from mp3s', command=self.extract_meta_data)
        extract_button.grid(row=2, column=0, sticky='nesw', pady=(40, 40), padx=(60, 60))

        if self.extracted:
            labeltext = "extracted length info from mp3s"
        else:
            labeltext = ""
        extract_label = ttk.Label(self.v, text=labeltext)
        extract_label.grid(row=3, column=0, sticky='nesw', pady=(40, 40), padx=(60, 60))

        insert_button = ttk.Button(self.v, text='insert meta data into '+self.app.m4aname, command=self.meta_into_m4a)
        insert_button.grid(row=4, column=0, sticky='nesw', pady=(40, 40), padx=(60, 60))

        if self.inserted:
            labeltext = "inserted chapter info into "+self.app.m4aname
        else:
            labeltext = ""
        extract_label = ttk.Label(self.v, text=labeltext)
        extract_label.grid(row=5, column=0, sticky='nesw', pady=(40, 40), padx=(60, 60))

        if self.inserted:
            quit_button = ttk.Button(self.v, text="quit", command=self.shutdown)
            quit_button.grid(row=6, column=0, sticky="news", pady=(40, 40), padx=(60, 60))

    def extract_meta_data(self):
        mp3s = self.app.files
        mp = vlc.MediaPlayer()
        length = []
        duration = 0
        for track in mp3s:
            self.app.load_media(track, mp)
            length = self.app.read_length(mp)
            track = Path(track).name
            name = track[:-len(".mp3")]  # in 3.9 use removesuffix('.mp3')
            self.app.write_metadata(str(self.app.album)+"_"+name, duration, length)
            duration += (length + 1)
        self.extracted = True
        self.v.destroy()
        self.app.show_view("meta")

    def meta_into_m4a(self):
        command = "ffmpeg -i "+str(self.app.output)+" -i "+str(self.app.metafile)+" -map_metadata 1 -codec copy "+str(self.app.m4aname)
        args = shlex.split(command)
        out = subprocess.run(args, capture_output=True)
        self.inserted = True
        self.v.destroy()
        self.app.show_view("meta")

    def shutdown(self):
        if self.app.listfile.exists():
            os.remove(self.app.listfile)
        if self.app.metafile.exists():
            os.remove(self.app.metafile)
        if self.app.output.exists():
            os.remove(self.app.output)

        self.app.root.destroy()
