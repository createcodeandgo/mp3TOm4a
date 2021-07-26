from tkinter import *
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk


class View(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)

    def show(self):
        '''Calling view will be visible.'''
        self.view()
        self.lift()

    def set_keys(self, root, d):
        '''
            Input: app instance
                   dict with keys and functions
            Bind app key input to functions.
        '''
        for key in d:
            func = d[key]
            root.bind(key, func)

    def view(self):
        '''
            Has to be implemented in child class.
            Define layout of the window.
        '''
        pass
