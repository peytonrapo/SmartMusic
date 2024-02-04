import mido
import numpy as np
from PIL import Image

def midi_to_array(midi_file):
    # Read the MIDI file
    midi = mido.MidiFile(midi_file)
    note_velocity = None

    # Define the time resolution (ticks per beat)
    ticks_per_beat = midi.ticks_per_beat

    # Create an empty array to represent the piano roll
    max_pitch = 127  # MIDI pitch ranges from 0 to 127
    piano_roll = np.zeros((max_pitch + 2, int(midi.length * ticks_per_beat * 2)))

    # Iterate through MIDI messages and fill the piano roll
    for track in midi.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            
            # Note-on event
            if msg.type == 'note_on' and msg.velocity > 0:
                
                note_velocity = msg.velocity
                piano_roll[msg.note, int(current_time)] = 255
            
            # note sustained or a rest; depends on whether a previous note_velocity was set
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if note_velocity is not None:
                    # Calculate note duration
                    for i in range(current_time - int(msg.time), current_time - 2):
                        # Write in the piano roll to represent the note's velocity (scaled from 127 to 255)
                        piano_roll[msg.note, i] = int(note_velocity) * 2 
                    # Reset note_start_time for the next note
                    note_velocity = None
                
            # add tempo as a line on the bottom
            if msg.type == 'set_tempo':
                for i in range(0, int(midi.length * ticks_per_beat * 2 - 1)):
                    piano_roll[127, i] = int(msg.tempo) / ticks_per_beat
            
    return piano_roll

def piano_roll_to_image(piano_roll):
    # Create an image from the piano roll
    image = Image.fromarray((piano_roll).astype('uint8'), 'L')

    # You can save the image if needed
    image.save('output_image.png')

    # You can also display the image using an external viewer
    image.show()

if __name__ == "__main__":
    midi_file_path = "test.mid"  # Replace with the path to your MIDI file
    piano_roll = midi_to_array(midi_file_path)
    piano_roll_to_image(piano_roll)
