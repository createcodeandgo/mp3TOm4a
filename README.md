# Introduction

Convert mp3s into one m4a file, including chapters and meta information based on the mp3 files.

ffmpeg is delicate with path names that contain white spaces or some special characters. Right now the program only works reliable, if the source path and the mp3 file names contain no white spaces. To work around that you can start the script from the mp3 directory. Then the file path is set to "." and you only have to check if your mp3 file names work out.

To extract the length of the mp3 files to get the chapter length, the program uses python-vlc: `pip install python-vlc`.