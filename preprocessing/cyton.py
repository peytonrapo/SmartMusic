# import time

# from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
# from brainflow.data_filter import DataFilter, DetrendOperations
from preprocessing import EEGDataProcessor

def main():
    # BoardShim.enable_dev_board_logger()

    # params = BrainFlowInputParams()
    # params.serial_port = "/dev/cu.usbserial-DP04WFTR"
    # board = BoardShim(BoardIds.CYTON_BOARD, params)

    # board.prepare_session()
    # board.start_stream()
    # BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    # time.sleep(10)
    # # nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    # data = board.get_board_data()
    # board.stop_stream()
    # board.release_session()

    # print(data)

    # # eeg_channels = board_descr['eeg_channels']
    # # # second eeg channel of synthetic board is a sine wave at 10Hz, should see huge alpha
    # # eeg_channel = eeg_channels[1]
    # # # optional detrend
    # # DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
    # # psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
    # #                                WindowOperations.BLACKMAN_HARRIS.value)

    # # band_power_alpha = DataFilter.get_band_power(psd, 7.0, 13.0)
    # # band_power_beta = DataFilter.get_band_power(psd, 14.0, 30.0)
    # # print("alpha/beta:%f", band_power_alpha / band_power_beta)
    eeg = EEGDataProcessor()
    eeg.start_session()
    raw_data = eeg.get_raw_data(15)
    print(raw_data)
    band_powers = eeg.data_preprocessing(raw_data)
    print(band_powers)


if __name__ == "__main__":
    main()