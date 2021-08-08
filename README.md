# Introduction

Convert mp3s into one m4a file, including chapters and meta information based on the mp3 files.

I tested it only on Ubuntu.

## Prerequisites
In the background the app uses the following software:
- [FFmpeg](https://www.ffmpeg.org/)
- [Sox](http://sox.sourceforge.net/sox.html)
- [Pysox](https://github.com/rabitt/pysox)

## Running the app
run `python mp3TOm4a.py` in the code folder

## Screenshots
![The start window. From top: a label "Turn you MP3s into one m4a file..". A label "Where are your MP3s?". A button "Find MP3s". A label "Where do you want to save the m4a file?". A button "Save m4a to..". A "Next" button.](screenshots/startscreen.png "Start Screen")

![A pop-up window saying "No MP3s selected". Question "Quit?" with buttons "Yes" and "No".](screenshots/noneselected.png "No MP3 selected")

![The conversion window. A button "start conversion".](screenshots/startconv.png "start conversion")

![A pop-up window saying "Finished". Question "Convert another one?" with "Yes" and "No" answers.](screenshots/finished.png "Finished conversion")
