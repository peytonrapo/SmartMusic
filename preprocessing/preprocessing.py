import time
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, AggOperations, WaveletTypes, NoiseEstimationLevelTypes, \
    WaveletExtensionTypes, ThresholdTypes, WaveletDenoisingTypes, WindowOperations, DetrendOperations


class EEGDataProcessor:
    def __init__(self, serial_port="/dev/cu.usbserial-DP04WFTR"):
        self.serial_port = serial_port
        BoardShim.enable_dev_board_logger()

        params = BrainFlowInputParams()
        params.serial_port = self.serial_port
        params.timeout = 30

        board_id = BoardIds.CYTON_DAISY_BOARD.value
        self.board_descr = BoardShim.get_board_descr(board_id)
        self.sampling_rate = int(self.board_descr['sampling_rate'])

        self.board = BoardShim(BoardIds.CYTON_DAISY_BOARD, params)

        print(self.board_descr['eeg_channels'])

    def start_session(self):
        self.board.prepare_session()

    def get_raw_data(self, length=15):
        self.board.start_stream()
        time.sleep(length)
        data = self.board.get_board_data()
        self.board.stop_stream()
        return data

    def data_preprocessing(self, data):
        band_powers = []

        nfft = DataFilter.get_nearest_power_of_two(self.sampling_rate)

        eeg_channels = self.board_descr['eeg_channels']

        df_before_processing = pd.DataFrame(np.transpose(data))
        plt.figure()
        df_before_processing[eeg_channels].plot(subplots=True)
        plt.savefig('before_processing.png')

        for count, channel in enumerate(eeg_channels):
            if count == 0:
                DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEAN.value)
            elif count == 1:
                DataFilter.perform_rolling_filter(data[channel], 3, AggOperations.MEDIAN.value)
            else:
                DataFilter.perform_wavelet_denoising(data[channel], WaveletTypes.BIOR3_9, 3,
                                                     WaveletDenoisingTypes.SURESHRINK, ThresholdTypes.HARD,
                                                     WaveletExtensionTypes.SYMMETRIC, NoiseEstimationLevelTypes.FIRST_LEVEL)

        df_after_processing = pd.DataFrame(np.transpose(data))
        plt.figure()
        df_after_processing[eeg_channels].plot(subplots=True)
        plt.savefig('after_processing.png')

        for eeg_channel in eeg_channels:
            DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
            psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, self.sampling_rate,
                                            WindowOperations.BLACKMAN_HARRIS.value)

            band_power_alpha = DataFilter.get_band_power(psd, 8.0, 12.0)
            band_power_beta = DataFilter.get_band_power(psd, 14.0, 30.0)
            band_power_gamma = DataFilter.get_band_power(psd, 30.0, 100.0)
            band_power_delta = DataFilter.get_band_power(psd, 0.5, 4.0)

            band_powers.append([band_power_alpha, band_power_beta, band_power_delta, band_power_gamma])
        band_powers = np.array(band_powers).flatten()
        print(band_powers.shape)
        return band_powers

    def end_session(self):
        self.board.release_session()

    def save_data(self, data, output_file="test"):
        with open(f'{output_file}-bandpower.csv', "w+") as my_csv:
            csv_writer = csv.writer(my_csv, delimiter=',')
            csv_writer.writerows(data)

        with open(f"{output_file}-raw.csv", "w+") as my_csv2:
            csv_writer = csv.writer(my_csv2, delimiter=',')
            csv_writer.writerows(data)
