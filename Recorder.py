# -*- coding: utf-8 -*-
"""
Estimate Relaxation from Band Powers

This example shows how to buffer, epoch, and transform EEG data from a single
electrode into values for each of the classic frequencies (e.g. alpha, beta, theta)
Furthermore, it shows how ratios of the band powers can be used to estimate
mental state for neurofeedback.

The neurofeedback protocols described here are inspired by
*Neurofeedback: A Comprehensive Review on System Design, Methodology and Clinical Applications* by Marzbani et. al

Adapted from https://github.com/NeuroTechX/bci-workshop
"""

if __name__ == "__main__":

    """ 3. GET DATA """
    # Set up
    print("Please enter name: ")
    name = input()
    if not os.path.isdir(name):
        os.mkdir(name)
    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')
    NUM_EPOCHS = 100
    for epoch in range(NUM_EPOCHS):
        # Get song from midi dataset
        dataset_path = 'new-trimmed-midi'
        genre = dataset_path + '/' + r.choice(os.listdir(dataset_path))
        subgenre = genre + '/' + r.choice(os.listdir(genre))
        artist = subgenre + '/' + r.choice(os.listdir(subgenre))
        song = artist + '/' + r.choice(os.listdir(artist))

        mixer.init()
        mixer.music.load(song)
        mixer.music.play()
        DATA_LENGTH = 10
        filename = str(round(time.time())) + '.csv'
        brainwaves_data = []
        try:
            # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
            while len(brainwaves_data) < DATA_LENGTH:
                """ 3.1 ACQUIRE DATA """
                # Obtain EEG data from the LSL stream
                eeg_data, timestamp = inlet.pull_chunk(
                    timeout=1, max_samples=int(SHIFT_LENGTH * fs))
                channel_data = []
                for INDEX_CHANNEL in range(NUM_CHANNELS):
                    # Only keep the channel we're interested in
                    ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]

                    # Update EEG buffer with the new data
                    eeg_buffer, filter_state = utils.update_buffer(
                        eeg_buffer, ch_data, notch=True,
                        filter_state=filter_state)

                    """ 3.2 COMPUTE BAND POWERS """
                    # Get newest samples from the buffer
                    data_epoch = utils.get_last_data(eeg_buffer,
                                                    EPOCH_LENGTH * fs)

                    # Compute band powers
                    band_powers = utils.compute_band_powers(data_epoch, fs)
                    band_buffer, _ = utils.update_buffer(band_buffer,
                                                        np.asarray([band_powers]))
                    # Compute the average band powers for all epochs in buffer
                    # This helps to smooth out noise
                    smooth_band_powers = np.mean(band_buffer, axis=0)

                    # print('Delta: ', band_powers[Band.Delta], ' Theta: ', band_powers[Band.Theta],
                    #       ' Alpha: ', band_powers[Band.Alpha], ' Beta: ', band_powers[Band.Beta])

                    """ 3.3 COMPUTE NEUROFEEDBACK METRICS """
                    # These metrics could also be used to drive brain-computer interfaces

                    # Alpha Protocol:
                    # Simple redout of alpha power, divided by delta waves in order to rule out noise
                    alpha_metric = smooth_band_powers[Band.Alpha] / \
                        smooth_band_powers[Band.Delta]
                    # print('Alpha Relaxation: ', alpha_metric)

                    # Beta Protocol:
                    # Beta waves have been used as a measure of mental activity and concentration
                    # This beta over theta ratio is commonly used as neurofeedback for ADHD
                    beta_metric = smooth_band_powers[Band.Beta] / \
                        smooth_band_powers[Band.Theta]
                    # print('Beta Concentration: ', beta_metric)

                    # Alpha/Theta Protocol:
                    # This is another popular neurofeedback metric for stress reduction
                    # Higher theta over alpha is supposedly associated with reduced anxiety
                    theta_metric = smooth_band_powers[Band.Theta] / \
                        smooth_band_powers[Band.Alpha]
                    # print('Theta Relaxation: ', theta_metric)
                    channel_data.extend([smooth_band_powers[Band.Alpha], smooth_band_powers[Band.Beta], smooth_band_powers[Band.Theta],smooth_band_powers[Band.Delta]])
                brainwaves_data.append(channel_data)
        except KeyboardInterrupt:
            print('Closing!')
        np.savetxt(name + '/' + filename, brainwaves_data, delimiter=',')
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
        df.to_csv(name + '/' + 'name2score.csv', mode='a', index=False, header=False)


# Skeleton code
# Util functions for data recorder should probably in the utils file
# Constructor:
    # Connect to EEG
    # Initialize buffers to record data
# Record data:
    # clear buffers
    # Play random song from song directory
    # query EEG buffer
    # return data for song
        # maybe timestamp the data? depends on how bad it is
# In terms of getting data for training that should probably be a different function that creates a recorder object


import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
import pandas as pd

import os
from pygame import mixer
import random as r
import time
import torch
from torch import nn
# Handy little enum to make code more readable


class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3

class Recorder:
    def __init__(self, bufferLength = 5, epochLength = 1, overlapLength = 0.0, numChannels = 4):
        """ EXPERIMENTAL PARAMETERS """
        # Modify these to change aspects of the signal processing
        # can make these into constructor

        # Length of the EEG data buffer (in seconds)
        # This buffer will hold last n seconds of data and be used for calculations
        self.BUFFER_LENGTH = bufferLength

        # Length of the epochs used to compute the FFT (in seconds)
        self.EPOCH_LENGTH = epochLength

        # Amount of overlap between two consecutive epochs (in seconds)
        self.OVERLAP_LENGTH = overlapLength

        # Amount to 'shift' the start of each next consecutive epoch
        self.SHIFT_LENGTH = self.EPOCH_LENGTH - self.OVERLAP_LENGTH

        # Index of the channel(s) (electrodes) to be used
        # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
        self.NUM_CHANNELS = numChannels

    def connect(self):
         # Search for active LSL streams
        print('Looking for an EEG stream...')
        streams = resolve_byprop('type', 'EEG', timeout=2)
        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')

        # Set active EEG stream to inlet and apply time correction
        print("Start acquiring data")
        inlet = StreamInlet(streams[0], max_buflen= BUFFER_LENGTH, max_chunklen=1)
        eeg_time_correction = inlet.time_correction()

        # Get the stream info and description
        info = inlet.info()
        description = info.desc()

        # Get the sampling frequency
        # This is an important value that represents how many EEG data points are
        # collected in a second. This influences our frequency band calculation.
        # for the Muse 2016, this should always be 256
        fs = int(info.nominal_srate())
        self.inlet = inlet

        # Initialize raw EEG data buffer
        self.eeg_buffer = np.zeros((int(fs * self.BUFFER_LENGTH), 1))
        self.filter_state = None  # for use with the notch filter

        # Compute the number of epochs in "buffer_length"
        n_win_test = int(np.floor((self.BUFFER_LENGTH - self.EPOCH_LENGTH) /
                                self.SHIFT_LENGTH + 1))

        # Initialize the band power buffer (for plotting)
        # bands will be ordered: [delta, theta, alpha, beta]
        self.band_buffer = np.zeros((n_win_test, 4))

    def getData():
        pass

