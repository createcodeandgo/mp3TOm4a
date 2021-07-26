from tkinter import *
from tkinter import ttk
from tkinter import filedialog
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

    def view(self):

        self.v = ttk.Frame(self.app.root, borderwidth=5, relief="ridge", width=600, height=600)
        self.v.grid(row=0, column=0, sticky="nswe")

        hello_label = ttk.Label(self.v, text='turn your mp3s into one m4a')
        hello_label.grid(row=0, column=0, sticky='nesw', pady=(10, 10), padx=(20, 20))

        source_label = ttk.Label(self.v, text='Where are the mp3s?')
        source_label.grid(row=1, column=0, sticky="new", pady=(10, 10), padx=(20, 20))

        source_button = ttk.Button(self.v, text='find mp3s', command=self.source)
        source_button.grid(row=2, column=0, sticky="new", pady=(10, 10), padx=(20, 20))

        if self.app.source_path.exists():
            text = self.app.source_path
        else:
            text = ""
        source_path_label = ttk.Label(self.v, text=text)
        source_path_label.grid(row=3, column=0, sticky="new", pady=(10, 10), padx=(20, 20))

        destination_label = ttk.Label(self.v, text='Where do you want to save the m4a?')
        destination_label.grid(row=4, column=0, sticky="new", pady=(10, 10), padx=(20, 20))

        destination_button = ttk.Button(self.v, text='save m4a to..', command=self.destination)
        destination_button.grid(row=5, column=0, sticky="new", pady=(10, 10), padx=(20, 20))

        destination_path_label = ttk.Label(self.v, text=self.app.dest_path)
        destination_path_label.grid(row=6, column=0, sticky="new", pady=(10, 10), padx=(20, 20))

        next_button = ttk.Button(self.v, text='next step', command=self.to_meta)
        next_button.grid(row=7, column=0, sticky="new", pady=(10, 10), padx=(20, 20))

    def source(self):
        types = [('mp3 files', '*.mp3')]
        self.get_rid_of_hiddenfiles()
        filelist = []

        files = filedialog.askopenfilenames(title='find mp3s', initialdir=self.sourcepath, filetypes=types)
        for f in files:
            filelist.append(Path(f))
        print(filelist)

        path = Path(filelist[0]).parent
        if Path.cwd() != Path(path):
            self.app.source_path = path.resolve()
            for f in filelist:
                self.app.files.append(Path(f))
        else:
            self.app.source_path = Path(".")
            for f in filelist:
                f = f.name
                print(f)
                self.app.files.append(Path(f))

        self.v.destroy()
        self.show()

    def destination(self):
        self.get_rid_of_hiddenfiles()

        path = filedialog.askdirectory(title='path for m4a', initialdir=self.app.source_path)
        if Path.cwd() != Path(path):
            self.app.dest_path = path.resolve()
        else:
            self.app.dest_path = Path(".")

        self.v.destroy()
        self.show()

    def get_rid_of_hiddenfiles(self):
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

    def to_meta(self):
        self.app.listfile = Path(self.app.dest_path, "list.txt")
        self.app.metafile = Path(self.app.dest_path, "meta.txt")
        self.app.output = Path(self.app.dest_path, "output.m4a")

        print(self.app.listfile)
        print(self.app.metafile)
        print(self.app.output)

        if self.app.listfile.exists():
            os.remove(self.app.listfile)
        if self.app.metafile.exists():
            os.remove(self.app.metafile)
        if self.app.output.exists():
            os.remove(self.app.output)

        self.v.destroy()
        self.app.show_view("concat")
