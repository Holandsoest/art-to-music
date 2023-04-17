from midiutil.MidiFile import MIDIFile

def MakeSong(list):
    #pitch, bpm, duration, volume, instrument, amount
    amount_of_instruments = len(list) # number of object on the screen 
    
    # define variables amount
    amount_of_piano = 0
    amount_of_drum = 0
    amount_of_guitar = 0
    amount_of_flute = 0
    amount_of_violin = 0
    amount_of_cello = 0

    object_piano = 0
    object_drum = 0
    object_guitar = 0
    object_flute = 0
    object_violin = 0
    object_cello = 0

    iteration = 0

    # determine the amount of shapes with the same instrument
    for shape in list:
        match shape.instrument:
            case 'piano':   amount_of_piano += 1
            case 'drum':    amount_of_drum += 1
            case 'guitar':  amount_of_guitar += 1
            case 'flute':   amount_of_flute += 1
            case 'violin':  amount_of_violin += 1
            case 'cello':   amount_of_cello += 1
            case _: pass
            
    print (amount_of_drum)
    # make midi file for every instrument
    midi_piano = MIDIFile(amount_of_piano, removeDuplicates=False)
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
            midi_drum.addTrackName(object_drum, time_drum, f"TrackDrum{object_drum}") # give track a name
            midi_drum.addTempo(object_drum, time_drum, shape.bpm) # set bpm
            midi_drum.addProgramChange(object_drum, 0, time_drum, 30) # add instrument = shape.instrument = 1
            midi_drum.addNote(object_drum, channel_drum, shape.pitch, time_drum, shape.duration, shape.volume) # make a note
            midi_drum.addNote(object_drum, channel_drum, 50, 2, 2, 255) # make a note
            
            object_drum +=1
        
        if amount_of_instruments -1 == iteration:
            #write all the midi files
            with open("piano_output.mid", "wb") as output_file:
                midi_piano.writeFile(output_file)
            with open("drum_output.mid", "wb") as output_file1:
                midi_drum.writeFile(output_file1)
            with open("guitar_output.mid", "wb") as output_file2:
                midi_guitar.writeFile(output_file2)
            with open("flute_output.mid", "wb") as output_file3:
                midi_flute.writeFile(output_file3)
            with open("violin_output.mid", "wb") as output_file4:
                midi_violin.writeFile(output_file4)
            with open("cello_output.mid", "wb") as output_file5:
                midi_cello.writeFile(output_file5)
            
        iteration += 1