# Example MultiLanguage Song Editor
Flask application to generate a .pro file that can be imported in pro-presenter 7.x and higher with multiple languages or translation(s)

introduction video for this web GUI: 
- https://youtu.be/31lTludJ2FQ


## Features

In this application you can 
- paste your song
- add group names like Verse 1, Chorus, etc
- put the translation next to the song text
- make sure the verse and chorus etc. line up for song and translation(s)
- click "Download .pro" to store it in the Download directory ( now you can import it into pro-presenter )


## Installation

### Requirements

python 3.10 or higher

`$ pip3 install -r requirements.txt`

This program needs a Template to know:
- how many languages or translations are used
- what the text box names are

To create this Template:
- Open pro-presenter 7 
- create a New Presentation with the name Template
- add the Text object for all required languages or translations
- Give all Text objects a unique name
- put them in the correct order in the Object list
- export the Presentation and copy it to web/kerk_naam1 this directory (replacing the current Template.pro file)


Group names:
- if you have created additional groups in pro-presenter, you can also add/remove them in this program
open the file GroupNames.txt and add/delete the group names

## Starting the application

```
install the pre-requisites,
$ cd \your foler name\ExampleMultiLanguageSongEditor
$ python3 flask_gui.py
```

or install it on a web hosting site that supports python 3.10 or higher and Flask.

one of the possible free hosting sites is https://www.pythonanywhere.com/ (has to be re-activated every 3 months)

## testing on a Windows 11 pc
Install python and pycharm
- https://www.youtube.com/watch?v=QhukcScB9W0
Running the song editor from pycharm
- https://youtu.be/mOeOMgsLrfg

