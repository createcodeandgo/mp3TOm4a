#!/usr/bin/python3

'''
    user can choose the source path with MP3 files
    user can choose the destination path for the m4a file
'''

#from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
from pathlib import Path

import view.parentview as view


class OpeningView(view.View):
    '''Show file window'''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app

        self.d = {}
        self.sourcepath = Path.cwd()
        self.destinationpath = Path.cwd()
        self.files = []
        self.stay = False

    def view(self):
        px = (100, 100)
        py = (25, 25)
        self.v = ttk.Frame(self.app.root, borderwidth=5, width=600, height=600)
        self.v.grid(row=0, column=0, columnspan=4)

        hello_label = ttk.Label(self.v, text='Turn your MP3s into one m4a file..')
        hello_label.grid(row=0, column=0, columnspan=4, sticky='nesw', pady=py, padx=px)

        source_label = ttk.Label(self.v, text='Where are the MP3s?')
        source_label.grid(row=1, column=0, columnspan=4, sticky="new", pady=py, padx=px)

        source_button = ttk.Button(self.v, text='Find MP3s', command=self.source)
        source_button.grid(row=2, column=0, columnspan=4, sticky="new", pady=py, padx=px)

        if self.app.source_path.exists():
            text = str(self.app.source_path)
        else:
            text = ""
        source_path_label = ttk.Label(self.v, text=text)
        source_path_label.grid(row=3, column=0, sticky="new", pady=py, padx=px)

        destination_label = ttk.Label(self.v, text='Where do you want to save the m4a file?')
        destination_label.grid(row=4, column=0, sticky="new", pady=py, padx=px)

        destination_button = ttk.Button(self.v, text='Save m4a to..', command=self.destination)
        destination_button.grid(row=5, column=0, sticky="new", pady=py, padx=px)

        destination_path_label = ttk.Label(self.v, text=self.app.dest_path)
        destination_path_label.grid(row=6, column=0, sticky="new", pady=py, padx=px)

        next_button = ttk.Button(self.v, text='Next', command=self.to_convert)
        next_button.grid(row=7, column=0, sticky="new", pady=(py), padx=px)
        
        if self.stay:
            self.todo = messagebox.askyesno('No MP3s selected', 'Quit?')
            if self.todo:
                self.app.root.destroy()
            else:
                self.stay = False

    def source(self):
        '''
            choose mp3s to concatenate
            set source path
        '''
        types = [('mp3 files', '*.mp3')]
        self.get_rid_of_hiddenfiles()
        filelist = []

        files = filedialog.askopenfilenames(title='find mp3s', initialdir=self.sourcepath, filetypes=types)
        for f in files:
            filelist.append(Path(f))

        if files:
            path = Path(filelist[0]).parent
        else:
            path = Path.cwd()

        if Path.cwd() != Path(path):
            self.app.source_path = path.resolve()
            for f in filelist:
                self.app.files.append(Path(f))
        else:
            self.app.source_path = Path(".")
            for f in filelist:
                f = f.name
                self.app.files.append(Path(f))

        self.app.dest_path = self.app.source_path

        self.v.destroy()
        self.show()

    def destination(self):
        '''
            set destination path for m4a
        '''
        self.get_rid_of_hiddenfiles()

        path = Path(filedialog.askdirectory(title='path for m4a', initialdir=self.app.source_path))
        if Path.cwd() != Path(path):
            self.app.dest_path = path.resolve()
        else:
            self.app.dest_path = self.app.source_path

        self.v.destroy()
        self.show()

    def get_rid_of_hiddenfiles(self):
        '''
            no hidden files in file dialog
        '''
        try:
            # call a dummy dialog with an impossible option to initialize the file
            # dialog without really getting a dialog window; this will throw a
            # TclError, so we need a try...except :
            try:
                self.app.root.tk.call('tk_getOpenFile', '-foobarbaz')
            except TclError:
                pass
            # now set the magic variables accordingly
            self.app.root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
            self.app.root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
        except:
            pass

    def to_convert(self):
        '''
            set paths to list.txt, meta.txt and temporary output m4a file
            delete those files if old ones are present
        '''
        if self.app.files != []:
            self.app.listfile = Path(self.app.dest_path, "list.txt")
            self.app.metafile = Path(self.app.dest_path, "meta.txt")
            self.app.output = Path(self.app.dest_path, "output.m4a")

            if self.app.listfile.exists():
                os.remove(self.app.listfile)
            if self.app.metafile.exists():
                os.remove(self.app.metafile)
            if self.app.output.exists():
                os.remove(self.app.output)

            self.v.destroy()
            self.app.show_view("convert")
        else:
            self.stay = True
            self.v.destroy()
            self.show()
