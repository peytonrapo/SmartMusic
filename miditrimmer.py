import os
import mido

MIDI_DATABASE_PATH = 'adl-piano-midi'
NEW_MIDI_DATABASE_PATH = 'trimmed-midi'
if not os.path.isdir(NEW_MIDI_DATABASE_PATH):
    os.mkdir(NEW_MIDI_DATABASE_PATH)
for genre in os.listdir(MIDI_DATABASE_PATH):
    if not os.path.isdir(NEW_MIDI_DATABASE_PATH + '/' + genre):
        os.mkdir(NEW_MIDI_DATABASE_PATH + '/' + genre)
    for subgenre in os.listdir(MIDI_DATABASE_PATH + '/' + genre):
        if not os.path.isdir(NEW_MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre):
            os.mkdir(NEW_MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre)
        for artist in os.listdir(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre):
            if not os.path.isdir(NEW_MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist):
                os.mkdir(NEW_MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist)
            for song in os.listdir(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist):
                try:
                    newSongPath = NEW_MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist + '/' + song
                    mid = mido.MidiFile(MIDI_DATABASE_PATH + '/' + genre + '/' + subgenre + '/' + artist + '/' + song) 
                    min_time = -1
                    if song == "Tango Korrupti.mid":
                        print('first pass')
                        print(len(mid.tracks))
                        print(mid.tracks[1])
                    for track in mid.tracks:
                        found = False
                        for msg in track:
                            if not found and msg.type == 'note_on':
                                if song == "Tango Korrupti.mid":
                                        print(msg.time)
                                if min_time == -1 or msg.time < min_time:
                                    min_time = msg.time
                                found = True
                    if song == "Tango Korrupti.mid":
                        print('second pass pass')
                    for track in mid.tracks:
                        found = False
                        for msg in track:
                            if not found:
                                if msg.type == 'note_on':
                                    msg.time -= min_time
                                    found = True
                                    if song == "Tango Korrupti.mid":
                                            print(msg.time)
                                else:
                                    msg.time = 0
                    newMid = mido.MidiFile()
                    newMid.ticks_per_beat = mid.ticks_per_beat
                    newMid.tracks.append(mido.merge_tracks(mid.tracks))
                    newMid.save(newSongPath)
                except:
                    print("Could not convert song" + song)
                