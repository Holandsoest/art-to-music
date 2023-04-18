from midiutil.MidiFile import MIDIFile
from midiutil.MidiFile import *
import os

def MakeSong(list):
    #pitch, bpm, duration, volume, instrument, amount
    amount_of_instruments = len(list) # number of object on the screen 
    model_custom_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
    
    # define variables amount
    amount_of_drum = 0
    amount_of_guitar = 0
    amount_of_flute = 0
    amount_of_violin = 0
    amount_of_cello = 0

    object_drum = 0
    object_guitar = 0
    object_flute = 0
    object_violin = 0
    object_cello = 0

    iteration = 0

    # determine the amount of shapes with the same instrument
    for shape in list:
        match shape.instrument:
            case 'drum':    amount_of_drum += 1
            case 'guitar':  amount_of_guitar += 1
            case 'flute':   amount_of_flute += 1
            case 'violin':  amount_of_violin += 1
            case 'cello':   amount_of_cello += 1
            case _: pass
            
    # make midi file for every instrument
    midi_drum = MIDIFile(amount_of_drum, removeDuplicates=False)    
    midi_guitar = MIDIFile(amount_of_guitar, removeDuplicates=False)
    midi_flute = MIDIFile(amount_of_flute, removeDuplicates=False)
    midi_violin = MIDIFile(amount_of_violin, removeDuplicates=False)
    midi_cello = MIDIFile(amount_of_cello, removeDuplicates=False)

    for shape in list:
        if amount_of_drum > 0 and shape.instrument == "drum":
            # add tracks
            time_drum = 0 # time to zero
            channel_drum = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_drum.addTrackName(object_drum, time_drum, f"Track{object_drum}") # give track a name
            midi_drum.addTempo(object_drum, time_drum, shape.bpm) # set bpm
            midi_drum.addProgramChange(object_drum, 0, time_drum, 1) # add instrument = shape.instrument = 1
            midi_drum.addNote(object_drum, channel_drum, shape.pitch, time_drum, shape.duration, shape.volume) # make a note

            object_drum +=1

        if amount_of_guitar > 0 and shape.instrument == "guitar":
            # add tracks
            time_guitar = 2 # time to zero
            channel_guitar = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_guitar.addTrackName(object_guitar, time_guitar, f"Track{object_guitar}") # give track a name
            midi_guitar.addTempo(object_guitar, time_guitar, shape.bpm) # set bpm
            midi_guitar.addProgramChange(object_guitar, 0, time_guitar, 1) # add instrument = shape.instrument = 1
            midi_guitar.addNote(object_guitar, channel_guitar, shape.pitch, time_guitar, shape.duration, shape.volume) # make a note

            object_guitar +=1

        if amount_of_flute > 0 and shape.instrument == "flute":
            # add tracks
            time_flute = 4 # time to zero
            channel_flute = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_flute.addTrackName(object_flute, time_flute, f"Track{object_flute}") # give track a name
            midi_flute.addTempo(object_flute, time_flute, shape.bpm) # set bpm
            midi_flute.addProgramChange(object_flute, 0, time_flute, 1) # add instrument = shape.instrument = 1
            midi_flute.addNote(object_flute, channel_flute, shape.pitch, time_flute, shape.duration, shape.volume) # make a note

            object_flute +=1

        if amount_of_violin > 0 and shape.instrument == "violin":
            # add tracks
            time_violin = 6 # time to zero
            channel_violin = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_violin.addTrackName(object_violin, time_violin, f"Track{object_violin}") # give track a name
            midi_violin.addTempo(object_violin, time_violin, shape.bpm) # set bpm
            midi_violin.addProgramChange(object_violin, 0, time_violin, 1) # add instrument = shape.instrument = 1
            midi_violin.addNote(object_violin, channel_violin, shape.pitch, time_violin, shape.duration, shape.volume) # make a note

            object_violin +=1
        
        if amount_of_cello > 0 and shape.instrument == "cello":
            # add tracks
            time_cello = 8 # time to zero
            channel_cello = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_cello.addTrackName(object_cello, time_cello, f"Track{object_cello}") # give track a name
            midi_cello.addTempo(object_cello, time_cello, shape.bpm) # set bpm
            midi_cello.addProgramChange(object_cello, 0, time_cello, 1) # add instrument = shape.instrument = 1
            midi_cello.addNote(object_cello, channel_cello, shape.pitch, time_cello, shape.duration, shape.volume) # make a note

            object_cello +=1
        
        if amount_of_instruments -1 == iteration:
            #write all the midi files
            with open(model_custom_path + "\\drum_output.mid", "wb") as output_file1:
                midi_drum.writeFile(output_file1)
            with open(model_custom_path + "\\guitar_output.mid", "wb") as output_file2:
                midi_guitar.writeFile(output_file2)
            with open(model_custom_path + "\\flute_output.mid", "wb") as output_file3:
                midi_flute.writeFile(output_file3)
            with open(model_custom_path + "\\violin_output.mid", "wb") as output_file4:
                midi_violin.writeFile(output_file4)
            with open(model_custom_path + "\\cello_output.mid", "wb") as output_file5:
                midi_cello.writeFile(output_file5)
            
        iteration += 1