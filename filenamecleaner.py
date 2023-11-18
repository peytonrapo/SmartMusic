import os

MIDI_DATABASE_PATH = "trimmed-midi"
for genre in os.listdir(MIDI_DATABASE_PATH):
    for subgenre in os.listdir(MIDI_DATABASE_PATH + '/' + genre):
        for artist in os.listdir(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre):
            for song in os.listdir(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist):
                trimmed_title = song.replace(" ", "-")
                os.rename(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist + '/' + song,
                MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist + '/' + trimmed_title)