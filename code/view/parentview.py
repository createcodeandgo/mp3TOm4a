from tkinter import *
from tkinter import ttk


class View(ttk.Frame):
    def __init__(self, app):
        ttk.Frame.__init__(self)
        
    def show(self):
        '''Calling view will be visible.'''
        self.view()
        self.lift()

    def view(self):
        '''
            Has to be implemented in child class.
            Define layout of the window.
        '''
        pass
