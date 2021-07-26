# Introduction

Convert mp3s into one m4a file, including chapters and meta information based on the mp3 files.

ffmpeg is delicate with path names that contain white spaces or some special characters. Right now the program works only reliable, if the source path and the mp3 file names contain no white spaces. To work around that you can start the script from the mp3 directory. Then the file path is set to "." and you only have to check if your mp3 file names work out.

## How to make it executable in any directory

To make this easier I followed these steps:
- put a link into ~/.local/bin path
`ln -s path/to/mp3tom4a.py mp3tom4a`
- made that link executable
`chmod 700 mp3tom4a
- made the mp3tom4a.py file executable
go to its directory and `chmod 700 mp3tom4a.py`
- add `#!/usr/bin/python3` as the first line in mp3tom4a.py

If ~/.local/bin is not part of your $PATH variable, you can add it with `PATH="~/.local/bin:$PATH"`.
