import numpy as np
import os
import matplotlib.pyplot as plt
import pylab
import csv
from scipy.signal import butter, sosfilt

# Set up the folder's path and pick the file to test
g_directory = "Ichi"
g_testingFile = "1698979544.csv"
g_lowcut = 0.5  # hz
g_highcut = 70  # hz
g_order = 5
g_times = 10

def csv_to_array(csv_reader):
    # Your existing code for csv_to_array
    line_count = 0
    brainwaves= [[]] * 16
    timepoints= [] * g_times

    for row in csv_reader:
            timepoints.append(line_count) 
            for x in range(16):
                brainwave = brainwaves[x].copy()
                brainwave.append(sci_to_int(row[x]))
                brainwaves[x]=brainwave
            line_count += 1
    return brainwaves, timepoints

def plot_graph(brainwavesData, timestamps):
    fig, ax = plt.subplots(16,1,figsize=(20,40))
    for x in range(16):
        # print(brainwavesData[x])
        ax[x].plot(timestamps, brainwavesData[x], label="waves "+str(x+1))

    plt.xlabel('time(s)')
    plt.ylabel('voltage')
    plt.title('eeg data')
    plt.show()

def sci_to_int(sci):
    number_as_float = float(sci)
    return "{:.2f}".format(number_as_float)  

def volts_to_freq(brainwavesData):
    blockSize = 10 #length of the signal
    timeInterval = 1
    samplingRate = 1/timeInterval
    frameSize = blockSize * timeInterval

    freqdata = [[]]*16
    index = 0

    for brainwave in brainwavesData:
        freq = np.arange(blockSize)/samplingRate
        freq = freq[range(int(blockSize/2))]
        SL = blockSize/2
        freqResol = freq/SL

        data = brainwave
        Y = np.fft.fft(data)/blockSize
        Y = Y[range(int(blockSize/2))]

        freqdata[index] = Y
        index=index+1
        plt.plot(freq,abs(Y),'r')
        plt.show
    return freqdata

def filtering(freqdata):
    filteredData = [[]]*16

    for i in range (16):
        freq = freqdata[i]
        nyquistFreq = 100
        low = g_lowcut / nyquistFreq
        high = g_highcut / nyquistFreq

        sos = butter(g_order, [low,high], btype = "bandpass", output='sos')
        filtered = sosfilt(sos, freq)

        filteredData[i] = filtered

    return filteredData


def plot_filtered_data(filteredData):
    blockSize = 10
    for i in range(16):
        filtered = filteredData[i]
        Y = np.fft.fft(filtered)/blockSize
        Y = Y[range(int(blockSize/2))]
        plt.plot(filtered, abs(Y),'r')

def array_to_csv(output_file, brainwaves, timepoints):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header (timepoints)
        csv_writer.writerow(timepoints)

        # Write the data (brainwaves)
        for i in range(len(brainwaves[0])):
            row_data = [brainwaves[x][i] for x in range(16)]
            csv_writer.writerow(row_data)

def main():
    print("start")
    # Iterate through the CSV file folder and draw separate graphs for each file
    for filename in os.listdir(g_directory):
        print("start2")
        f = os.path.join(g_directory, filename)

        # Checking if it is the file we are testing
        if os.path.isfile(f):
            if filename != "name2score.csv":  # Just one file for testing for now
                print("Current filepath: " + f)
                with open(f) as csv_file:
                    # Plotting the raw data (voltage)
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    brainwavesData, timepoints = csv_to_array(csv_reader)
                    #plot_graph(brainwavesData, timepoints)

                    # Convert the data from voltage to frequency + plotting the graph
                    freqdata = volts_to_freq(brainwavesData)

                    # Filter the frequency data
                    filtereddata = filtering(freqdata)
                    #plot_filtered_data(filtereddata)

                    #save processed data to the same file
                    output_csv_file = os.path.join(g_directory, "output_"+filename)
                    array_to_csv(output_csv_file, filtereddata, timepoints)
                    print(f"Reversed data saved to {output_csv_file}")

if __name__ == "__main__":
    main()
