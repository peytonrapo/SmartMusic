# IMPORT
# imports from utils.py, etc.
import threading
from utils import get_random_file

# SET MACROS
# ex: index_channels for recording, buffer_size.

# MUSE/OPENBCI SET UP
# Establish EEG stream.
# code here

# CALIBRATION CYCLE
# Online training.
# Loop until threshold_accuracy reached:    
# # Play music and record data. Predict whether user liked music, user inputs ground truth.
# # Update model.

classifier = None
music_gen = None
threshold_accuracy = 0.75

while True:
    
    # ----- play music and record EEG
    music =  get_random_file('new-trimmed-midi') # select song
    
    play_song_thread = threading.Thread(target=play_song, args=(music,))
    record_thread = threading.Thread(target=record)
    
    play_song_thread.start()
    record_thread.start()
    
    play_song_thread.join()
    recorded_data = record_thread.join()  # get data from recording
    
    cleaned_recording = build_input_tensor(recorded_data)  # clean data
    
    # ------ predict user response and compare to ground truth
    prediction = classifier.predict(cleaned_recording)
    
    ground_truth = int(input("Did you like the music? (1 for yes, 0 for no): "))
    
    current_accuracy = compute_accuracy(ground_truth, prediction)
    
    print(f"Current Accuracy: {current_accuracy}")
    
    if current_accuracy >= threshold_accuracy:
        print("Threshold accuracy reached. Calibration cycle complete.")
        break


# MAIN 
# Constantly play music and record data

prev_song = music
prediction = ground_truth  # for the first time we enter post calibration, we have ground truth
pred_total = 0

while True:
    music_gen = music_gen.predict(prediction, prev_song)  # generate new song
    play_song_thread = threading.Thread(target=play_song, args=(music_gen,))
    record_thread = threading.Thread(target=record)
    
    play_song_thread.start()
    record_thread.start()
    
    play_song_thread.join()
    recorded_data = record_thread.join()  # get data from recording
    
    prediction = classifier.predict(recorded_data)
    print("Prediction: {prediction}")
    pred_total += prediction
    
    if pred_total > 4:
        print('Generated 5 good songs.')
        break