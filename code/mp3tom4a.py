#!/usr/bin/python3

from pathlib import Path
from tkinter import Tk
from tkinter import ttk
from PIL import Image, ImageTk

from view.opening import OpeningView
from view.convert import ConvertView


class Converter():
    def __init__(self, root: Tk):
        super().__init__()
        self.root = root
        self.root.grid()
        self.root.title("mp3s to m4a")

        mainframe = ttk.Frame(self.root,
                              relief="ridge",
                              width=600,
                              height=600)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        mainframe.grid(row=0, column=0, sticky="nswe")

        self.files: Path = []
        self.dest_path = Path(".")
        self.source_path = Path(".")
        self.listfile: Path
        self.metafile: Path
        self.output: Path

        self.opening = OpeningView(self)
        self.convert = ConvertView(self)

        self.view_dict = {"opening": self.opening,
                          "convert": self.convert}

        self.opening.show()

    def show_view(self, viewname):
        frame = self.view_dict[viewname]
        frame.show()


def main():
    try:
        root = Tk()
        ico = Image.open('mp3TOm4a.png')
        photo = ImageTk.PhotoImage(ico)
        root.wm_iconphoto(False, photo)
        Converter(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("keyboard interrupt")

if __name__ == "__main__":
    main()
