import os

MIDI_DATABASE_PATH = "trimmed-midi"
NEW_MIDI_DATABASE = "new-trimmed-midi"
for genre in os.listdir(MIDI_DATABASE_PATH):
    trimmed_genre = genre.replace(" ", "-")
    if not os.path.isdir(NEW_MIDI_DATABASE + '/' + trimmed_genre):
        os.mkdir(NEW_MIDI_DATABASE + '/' + trimmed_genre)
    for subgenre in os.listdir(MIDI_DATABASE_PATH + '/' + genre):
        trimmed_subgenre = subgenre.replace(" ", "-")
        if not os.path.isdir(NEW_MIDI_DATABASE + '/' + trimmed_genre + '/' + trimmed_subgenre):
            os.mkdir(NEW_MIDI_DATABASE + '/' + trimmed_genre + '/' + trimmed_subgenre)
        for artist in os.listdir(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre):
            trimmed_artist = artist.replace(" ", "-")
            if not os.path.isdir(NEW_MIDI_DATABASE + '/' + trimmed_genre + '/' + trimmed_subgenre + '/' + trimmed_artist):
                os.mkdir(NEW_MIDI_DATABASE + '/' + trimmed_genre + '/' + trimmed_subgenre + '/' + trimmed_artist)
            for song in os.listdir(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist):
                trimmed_title = song.replace(" ", "-")
                os.rename(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist + '/' + song,
                NEW_MIDI_DATABASE + '/' + trimmed_genre + '/' + trimmed_subgenre + '/' + trimmed_artist + '/' + trimmed_title)