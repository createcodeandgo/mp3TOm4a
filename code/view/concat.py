from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path

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


        if self.intro:
            button_text = 'start'
        else:
            button_text = 'writing to '+str(self.app.output)

        conv_button = ttk.Button(self.v, text=button_text, command=self.concat)
        conv_button.grid(row=2, column=0, sticky="new", pady=(40, 40), padx=(60, 60))

    def concat(self):
        self.intro = False
        # starts meta.txt files with general tag info
        # writes mp3 files to concat into list.txt
        meta_out = str(self.app.get_filelist())
        print(meta_out)
        if meta_out.endswith("directory\n"):
            print("error with writing meta file, maybe spaces in path?")
            self.app.root.destroy()
        self.app.read_metafile()
        self.app.m4aname = str(self.app.dest_path)+"/"+str(self.app.album)+".m4a"
        cat_out = str(self.app.concatenatemp3s())
        self.v.destroy()
        self.show()

        if cat_out.startswith("CompletedProcess"):
            self.v.destroy()
            self.app.show_view("meta")
        else:
            self.v.destroy()
            self.app.show_view("caterror")
