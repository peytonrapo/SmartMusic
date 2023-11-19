import numpy as np
import os
import matplotlib.pyplot as plt
import pylab
import csv
from scipy.signal import butter, sosfilt

#set up the folder's path and pick the file to test
g_directory = "/Users/rubylee/SmartMusic-1/Ichi"
g_testingFile = "1698979544.csv"

g_lowcut = 0.5 #hz
g_highcut = 70 #hz
g_order = 5

# csv_to_array: convert the csv to a timestamp array and a list containing 16 arrays
def csv_to_array(csv_reader):
    line_count = 0
    brainwaves= [[]]*16
    timepoints= [] * 10

    for row in csv_reader:
            timepoints.append(line_count) 
            for x in range(16):
                brainwave = brainwaves[x].copy()
                brainwave.append(sci_to_int(row[x]))
                brainwaves[x]=brainwave
            line_count += 1
    return brainwaves, timepoints

# plot_graph: draw the graph with 16 lines representing different channel/brain-waves combinations
def plot_graph(brainwavesData, timestamps):
    fig, ax = plt.subplots(16,1,figsize=(20,40))
    for x in range(16):
        # print(brainwavesData[x])
        ax[x].plot(timestamps, brainwavesData[x], label="waves "+str(x+1))

    plt.xlabel('time(s)')
    plt.ylabel('voltage')
    plt.title('eeg data')
    plt.show()

# sci_to_int: convert scientific notation string to int
def sci_to_int(sci):
    number_as_float = float(sci)
    return "{:.2f}".format(number_as_float)    

# volts_to_freq: covert the graph from time domain to frequency domain using discrete 
#             fourier transform the command numpy.fft.fft(SIGNAL)
def volts_to_freq(brainwavesData):   
    blockSize = 10 #length of the signal
    timeInterval = 1
    samplingRate = 1/timeInterval
    frameSize = blockSize * timeInterval

    freqdata = [[]]*16
    index = 0

    for brainwave in brainwavesData():
        freq = np.arrange(blockSize)/samplingRate
        freq = freq[range(int(blockSize/2))]
        #SL: spectral line
        SL = blockSize/2
        freqResol = freq/SL

        data = brainwave
        Y = np.fft.fft(data)/blockSize
        Y = Y[range(int(blockSize/2))]

        freqdata[index] = Y
        plt.plot(freq,abs(Y),'r')
        plt.show

    return freqdata

#filtering: using butterworth to filter out the noises in the raw data
def filtering(freqdata):
    filteredData = [[]]*16

    for i in range (16):
        freq = freqdata[i]
        nyquistFreq = 
        low = g_lowcut / nyquistFreq
        high = g_highcut / nyquistFreq
        sos = butter(g_order, [low,high], btype = "bandpass", output='sos')
        filtered = sosfilt(sos, freq)
        filteredData[i] = filtered
    return filteredData

#plotting the filtered data
def plot_filtered_data(filteredData):
    blockSize = 10
    for i in range(16):
        filtered = filteredData[i]
        Y = np.fft.fft(filtered)/blockSize
        Y = Y[range(int(blockSize/2))]
        plt.plot(filtered, abs(Y),'r')

# - - - - - - - - - - - - - - - - - main - - - - - - - - - - - - - - - - - - - - 
# iterate through the csv file folder and drawing seperate graphs for each file
for filename in os.listdir(g_directory):

    f = os.path.join(g_directory, filename)
    if filename=="name2score.csv": #skip the name2score file
        continue

    # checking if it is a file
    if os.path.isfile(f):
        if filename==g_testingFile: #just 1 file for testing for now
            print("current filepath: "+f)
            with open(f) as csv_file:

                #plotting the raw data (voltage)
                csv_reader = csv.reader(csv_file, delimiter=',')
                brainwavesData, timepoints = csv_to_array(csv_reader) 
                plot_graph(brainwavesData, timepoints) 

                #convert the data from voltage to frequency + plotting the graph
                freqdata = volts_to_freq(brainwavesData)

                #filter the frequency data
                filtereddata = filtering(freqdata)


