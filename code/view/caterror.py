from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from pathlib import Path

import view.parentview as view


class CaterrorView(view.View):
    '''Show file window'''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app

        self.d = {}

    def view(self):
        #self.set_keys(self.app.root, self.d)

        self.v = ttk.Frame(self.app.root, borderwidth=5, relief="ridge", width=600, height=600)
        self.v.grid(row=0, column=0, sticky="nswe")

        errortext = self.app.cat_out

        hello_label = ttk.Label(self.v, text=errortext)
        hello_label.grid(row=0, column=0, sticky='nesw', pady=(40,40), padx=(60,60))
