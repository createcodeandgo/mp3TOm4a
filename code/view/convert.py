#!/usr/bin/python3

'''
    Button press starts the conversion of the MP3s.
    After it is finished a pop-up window lets the user
    choose to quit or convert more.    
'''

from tkinter import *
from tkinter import ttk
import os
from pathlib import Path
import shlex
import subprocess
import sox

import view.parentview as view


class ConvertView(view.View):
    '''Show Convert window'''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app
        
        self.concatenated = False
        self.extracted = False
        self.inserted = False
        self.todo = False
        
        self.d = {}

    def view(self):
        self.v = ttk.Frame(self.app.root, borderwidth=5, relief="ridge", width=600, height=600)
        self.v.grid(row=0, column=0, sticky="nswe")

        conv_button = ttk.Button(self.v, text="start conversion", command=self.start_concat)
        conv_button.grid(row=1, column=0, columnspan=2, sticky="news", pady=(40, 40), padx=(60, 60))
                
        if self.inserted and self.extracted:
            self.todo = messagebox.askyesno('Finished', 'Convert another one?')
            if self.todo:
                self.concatenated = False
                self.extracted = False
                self.inserted = False
                self.todo = False
                self.v.destroy()
                self.app.show_view("opening")
            else:
                self.shutdown()
        
    def start_concat(self):
        '''
            write mp3 files to list.txt
            write meta info into meta.txt
            concatenate mp3s into one m4a
            get length of mp3s and write into meta.txt
            write chapter info into m4a
        '''
        self.intro = False
        
        meta_out = str(self.get_filelist())
        
        self.get_albumname()
        self.app.m4aname = Path(self.app.dest_path, str(self.app.album)+".m4a")
        cat_out = str(self.concatenate_mp3s())
        self.concatenated = True
                
        self.extract_length()
        self.extracted = True
        
        self.meta_into_m4a()
        self.inserted = True
        self.todo = True
        
    def get_filelist(self):
        '''
            read meta data from the first file selected
            save it in meta.txt
            write all mp3 filenames into list.txt
        '''
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

    def get_albumname(self):
        '''
            read album name from meta file
        '''
        with open(self.app.metafile, 'r') as f:
            for line in f:
                info = line.split('=')
                if info[0] == 'album':
                    album = info[1].strip("\n")
                    self.app.album = Path(album)
                    break

    def concatenate_mp3s(self):
        '''
            run ffmpeg to concatenate the mp3s into one m4a
        '''
        listfile = shlex.quote(str(self.app.listfile))
        print("listfile: ",repr(listfile))
        listfile = listfile.strip()
        output = shlex.quote(str(self.app.output))
        print("output: ",output)
        command = "ffmpeg -f concat -safe 0 -i {} -acodec aac -vn {}".format(listfile, output)
        args = shlex.split(command)
        for item in args:
            item = item.strip()
        print("args: -------------> ",repr(args))
        cat_out = subprocess.run(args, capture_output=True)
        print("concat -----------> ",cat_out)
        return cat_out
    
    def extract_length(self):
        '''
            use sox to read length from mp3s
        '''
        mp3s = self.app.files
        length = []
        duration = 0
        for track in mp3s:
            l = sox.file_info.duration(track)
            length = int(l*1000)
            track = Path(track).name
            name = track[:-len(".mp3")]  # in 3.9 use removesuffix('.mp3')
            self.write_metadata(str(self.app.album)+"_"+name, duration, length)
            duration += (length + 1)
        self.extracted = True

    def write_metadata(self, track, end, length):
        '''
            write general meta info into meta.txt
            info taken from first mp3 in file list
        '''
        with open(self.app.metafile, 'a') as f:
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

    def meta_into_m4a(self):
        '''
            add chapter information from meta.txt into m4a file
        '''
        output = shlex.quote(str(self.app.output))
        meta = shlex.quote(str(self.app.metafile))
        m4a = shlex.quote(str(self.app.m4aname))
        print("m4a file: ",m4a)
        command = "ffmpeg -i {} -i {} -map_metadata 1 -codec copy {}".format(output, meta, m4a)
        print(command)
        args = shlex.split(command)
        out = subprocess.run(args, capture_output=True)
        print("metadata in ---> ",out)
        self.inserted = True
        
    def shutdown(self):
        if self.app.listfile.exists():
            os.remove(self.app.listfile)
        if self.app.metafile.exists():
            os.remove(self.app.metafile)
        if self.app.output.exists():
            os.remove(self.app.output)

        self.app.root.destroy()
