import time

# from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
# from brainflow.data_filter import DataFilter, DetrendOperations
import numpy as np
from pygame import mixer
import pandas as pd
import random as r
import os

from preprocessing import EEGDataProcessor

def get_random_song():
    # Get song from midi dataset 
    dataset_path = '../new-trimmed-midi'
    genre = dataset_path + '/' + r.choice(os.listdir(dataset_path))
    subgenre = genre + '/' + r.choice(os.listdir(genre))
    artist = subgenre + '/' + r.choice(os.listdir(subgenre))
    song = artist + '/' + r.choice(os.listdir(artist))
    return song

def main():
    eeg = EEGDataProcessor()
    eeg.start_session()

    for i in range(10):
        song = get_random_song()

        # play song
        mixer.init()
        mixer.music.load(song)
        mixer.music.play()

        filename = 'classifier_training_data/' + str(round(time.time())) + '.csv'

        try:
            raw_data = eeg.get_raw_data(15)
            print(raw_data)
            band_powers = eeg.data_preprocessing(raw_data)
            print(band_powers)
            eeg.save_data(eeg.data_preprocessing(raw_data))
            
        except KeyboardInterrupt:
            print('Closing!')
        # np.savetxt(filename, band_powers, delimiter=',')
        # eeg.save_data(raw_data, filename)
        eeg.save_data(band_powers, filename)
        mixer.music.stop()
        print("Did you like the song? Y/N")
        val = input()
        score = 0.0
        while(val != 'Y' and val != 'N'):
            val = input()
        if val == 'Y':
            score = 1.0
        admin_data = {
            "filename":filename,
            "score":score
        }
        df = pd.DataFrame(admin_data, index=[0])
        df.to_csv('classifier_training_data/name2score.csv', mode='a', index=False, header=False)

if __name__ == "__main__":
    main()