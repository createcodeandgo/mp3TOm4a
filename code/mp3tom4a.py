#!/usr/bin/python3

import vlc
import os
import time
import subprocess
import shlex
from pathlib import Path
from tkinter import *
from tkinter import ttk

from view.opening import OpeningView
from view.concat import ConcatView
from view.meta import MetaView


class Converter():
    def __init__(self, root: Tk):
        super().__init__()
        self.root = root
        self.root.grid()
        self.root.title("mp3s to m4a")

        mainframe = ttk.Frame(self.root,
                              padding="10 10 10 10",
                              width=600,
                              height=600)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        mainframe.grid(row=0, column=0, sticky="nswe")

        self.files: Path = []
        self.dest_path = Path(".")
        self.source_path = Path(".")
        self.cat_out = ""
        self.meta_out = ""
        self.m4aname: Path
        self.listfile: Path
        self.metafile: Path
        self.output: Path
        self.album: Path

        self.opening = OpeningView(self)
        self.concat = ConcatView(self)
        self.meta = MetaView(self)

        self.view_dict = {"opening": self.opening,
                          "concat": self.concat,
                          "meta": self.meta}

        self.opening.show()

    def show_view(self, viewname):
        frame = self.view_dict[viewname]
        frame.show()

    def get_filelist(self):
        command = "ffmpeg -i "+str(self.files[0])+" -f ffmetadata "+str(self.metafile)
        args = shlex.split(command)
        meta_out = subprocess.run(args, capture_output=True)
        for mp3 in self.files:
            with open(str(self.listfile), 'a') as f:
                f.write("file '"+str(mp3)+"'\n")
        return meta_out

    def concatenatemp3s(self):
        # run ffmpeg to concatenate the mp3s into one m4a
        command = "ffmpeg -f concat -safe 0 -i "+str(self.listfile)+" -acodec aac -vn "+str(self.output)
        args = shlex.split(command)
        cat_out = subprocess.run(args, capture_output=True)
        return cat_out

    def read_metafile(self):
        temp = ""
        with open(self.metafile, 'r') as f:
            for line in f:
                info = line.split('=')
                if info[0] == 'album':
                    album = info[1]
                    for c in album:
                        if c.isalnum():
                            temp += c
                    self.album = Path(temp)

    def load_media(self, audio, mp):
        media = vlc.Media(audio)
        mp.set_media(media)

    def read_length(self, mediaplayer):
        mediaplayer.play()
        time.sleep(1)
        length = mediaplayer.get_length()
        mediaplayer.stop()
        return length

    def get_all_files(self):
        files = sorted([f for f in os.listdir(".")
                       if f.endswith(".mp3")],
                       key=str.lower)
        return files

    def write_metadata(self, track, end, length):
        with open(self.metafile, 'a') as f:
            f.write('\n')
            f.write('[CHAPTER]\n')
            f.write('TIMEBASE=1/1000\n')
            f.write('START='+str(end)+'\n')
            end = end + length
            f.write('END='+str(end)+'\n')
            f.write('title='+track+'\n')
            secs = length // 1000
            mins = secs // 60
            secs = secs % 60
            f.write('#chapter duration 00:'+str(mins)+':'+str(secs)+'\n')


def main():
    try:
        root = Tk()
        conv = Converter(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("meta*******************************")
        print(conv.meta_out)
        print("cat*******************************")
        print(conv.cat_out)


if __name__ == "__main__":
    main()
