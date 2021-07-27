from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path
import shlex
import subprocess

import view.parentview as view


class ConcatView(view.View):
    '''Show file window'''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app

        self.intro = True

        self.d = {}

    def view(self):
        self.v = ttk.Frame(self.app.root, borderwidth=5, relief="ridge", width=600, height=600)
        self.v.grid(row=0, column=0, sticky="nswe")

        hello_label = ttk.Label(self.v, text='start the conversion')
        hello_label.grid(row=0, column=0, sticky='nesw', pady=(40, 40), padx=(60, 60))

        conv_button = ttk.Button(self.v, text="start", command=self.concat)
        conv_button.grid(row=2, column=0, sticky="new", pady=(40, 40), padx=(60, 60))

    def concat(self):
        '''
            concatenate mp3 into one m4a file with ffmpeg
        '''
        self.intro = False
        # starts meta.txt files with general tag info
        # writes mp3 files to concat into list.txt
        meta_out = str(self.get_filelist())
        self.read_metafile()
        self.app.m4aname = Path(self.app.dest_path, str(self.app.album)+".m4a")
        cat_out = str(self.concatenatemp3s())
        self.v.destroy()
        self.app.show_view("meta")

    def get_filelist(self):
        # read meta data from the first file selected
        # save it in meta.txt
        audiofile = shlex.quote(str(self.app.files[0]))
        meta = shlex.quote(str(self.app.metafile))
        command = "ffmpeg -i {} -f ffmetadata {}".format(audiofile,meta)
        args = shlex.split(command)
        meta_out = subprocess.run(args, capture_output=True)
        # save selected file names in list.txt
        for mp3 in self.app.files:
            with open(self.app.listfile, 'a') as f:
                f.write("file '"+str(mp3)+"'\n")
        return meta_out

    def read_metafile(self):
        '''
            read album name from meta file
        '''
        temp = ""
        with open(self.app.metafile, 'r') as f:
            for line in f:
                info = line.split('=')
                if info[0] == 'album':
                    album = info[1].strip("\n")
                    #for c in album:
                    #    if c.isalnum():
                    #        temp += c
                    self.app.album = Path(album)
                    break

    def concatenatemp3s(self):
        # run ffmpeg to concatenate the mp3s into one m4a
        listfile = shlex.quote(str(self.app.listfile))
        output = shlex.quote(str(self.app.output))
        command = "ffmpeg -f concat -safe 0 -i {} -acodec aac -vn {}".format(listfile, output)
        args = shlex.split(command)
        cat_out = subprocess.run(args, capture_output=True)
        return cat_out
