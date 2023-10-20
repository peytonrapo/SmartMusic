import random as r
import os
from pygame import mixer
import time

dataset_path = 'adl-piano-midi'
genre = dataset_path + '/' + r.choice(os.listdir(dataset_path))
subgenre = genre + '/' + r.choice(os.listdir(genre))
artist = subgenre + '/' + r.choice(os.listdir(subgenre))
song = artist + '/' + r.choice(os.listdir(artist))
print(song)
mixer.init()
mixer.music.load(song)
mixer.music.play()
time.sleep(5)