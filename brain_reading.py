# IMPORT
# imports from utils.py, etc.

import multiprocessing
from utils import get_random_file
from utils import Recorder
from utils import Generator

# SET MACROS
# ex: index_channels for recording, buffer_size.

# MUSE/OPENBCI SET UP
# Establish EEG stream.
# code here

# CALIBRATION CYCLE
# Online training.
# Loop until threshold_accuracy reached:    
# # Play music from database and record data. Predict whether user liked music, user inputs ground truth.
# # Update model.

classifier = None
music_gen = None
threshold_accuracy = 0.75

# Initialize the queues
recording_queue = multiprocessing.Queue()
generation_queue = multiprocessing.Queue()

# generator is set calibrate = True so songs are classified but not generated
recording_process = multiprocessing.Process(target=Recorder(recording_queue, generation_queue))
generator_process = multiprocessing.Process(target=Generator(recording_queue, generation_queue, calibrate = True))

recording_process.start()
generator_process.start()

while True:
    
    # ----- play music and record EEG
    music1 = get_random_file('new-trimmed-midi') # select song (may select the same song per loop - fix or?)
    recording_queue.put(music1) 

    # ------ predict user response and compare to ground truth
    recording_process.join()
    generator_process.join()
    
    ground_truth = int(input("Did you like the music? (1 for yes, 0 for no): "))
    
    current_prediction = generator_process.get_prediction()
    current_accuracy = compute_accuracy(ground_truth, current_prediction)
    
    print(f"Current Accuracy: {current_accuracy}")
    
    if current_accuracy >= threshold_accuracy:
        print("Threshold accuracy reached. Calibration cycle complete.")
        break


# MAIN 
# Constantly generate and play music and record data
prediction = ground_truth  # for the first time we enter post calibration, we have ground truth
pred_total = 0

# Start a new generation queue with calibrate_mode false
generation_queue = multiprocessing.Queue()
generator_process = multiprocessing.Process(target=Generator(recording_queue, generation_queue))

generator_process.start()

while True:
    # Initialize queue with 2 songs (generator starts generating song 3 while song 2 is playing)
    song_buffer1 = get_random_file('new-trimmed-midi') 
    song_buffer2 = get_random_file('new-trimmed-midi', song_buffer1)

    recording_queue.put(song_buffer1)
    recording_queue.put(song_buffer2)

    recording_process.join()
    generator_process.join()

    current_prediction = generator_process.get_prediction()  
    print("Prediction: {current_prediction}")
    pred_total += prediction
    
    if pred_total > 4:
        print('Generated 5 good songs.')
        break