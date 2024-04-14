import argparse
import time
import csv

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, \
    Wavel
etExtensionTypes, ThresholdTypes, WaveletDenoisingTypes, WindowOperations, DetrendOperations


def getData(length = 15, outputFile = "test"):
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.serial_port = "/dev/cu.usbmodem11"
    params.timeout = 30

    board_id = BoardIds.GANGLION_BOARD.value
    board_descr = BoardShim.get_board_descr(board_id)
    sampling_rate = int(board_descr['sampling_rate'])
    
    board = BoardShim(BoardIds.GANGLION_BOARD, params)
    board.prepare_session()
    board.start_stream ()

    time.sleep(length)
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    print(sampling_rate)
    # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    data = board.get_board_data()  # get all data and remove it from internal buffer
    
    board.stop_stream()
    board.release_session()

    print(data)


    #denoising
    eeg_channels = BoardShim.get_eeg_channels(board_id)
    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels].plot(subplots=True)
    plt.savefig('before_processing.png')

    # dapply different methods to different channels for demo
    for count, channel in enumerate(eeg_channels):
        # first try simple moving median or moving average with different window size
        if count == 0:
            DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEAN.value)
        elif count == 1:
            DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEDIAN.value)
        # if methods above dont work, wavelet based denoising
        else:
            DataFilter.perform_wavelet_denoising(data[channel], WaveletTypes.BIOR3_9, 3,
                                                 WaveletDenoisingTypes.SURESHRINK, ThresholdTypes.HARD,
                                                 WaveletExtensionTypes.SYMMETRIC, NoiseEstimationLevelTypes.FIRST_LEVEL)

    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels].plot(subplots=True)
    plt.savefig('after_processing.png')


    eeg_channels = board_descr['eeg_channels']

    #filtering

    rows = [] 
    with open(f'{outputFile}-bandpower.csv',"w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        row = [] 
        print(len(data))
        print(len(data[0]))
        print(len(eeg_channels))
        for i in range (len(eeg_channels)):
            eeg_channel = eeg_channels[i]
            DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
            psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                        WindowOperations.BLACKMAN_HARRIS.value)

            #delta (0.5–4 Hz), theta (4–8 Hz), alpha (8–12 Hz), beta (12–30 Hz), and gamma (30–100 Hz)
            band_power_alpha = DataFilter.get_band_power(psd, 8.0, 12.0)
            band_power_beta = DataFilter.get_band_power(psd, 14.0, 30.0)
            band_power_gamma= DataFilter.get_band_power(psd, 30.0, 100.0)
            band_power_delta = DataFilter.get_band_power(psd, 0.5, 4.0)
            
            row.extend([band_power_alpha, band_power_beta, band_power_delta, band_power_gamma])
        rows.append(row)
        csvWriter.writerows(rows)

    with open(f"{outputFile}-raw.csv","w+") as my_csv2: 
        csvWriter = csv.writer(my_csv2,delimiter=',')
        csvWriter.writerows(data)


