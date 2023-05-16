from midiutil.MidiFile import MIDIFile
from midiutil.MidiFile import *
import os

def MakeSong(list):

    # --- define functions ---
    def forbidden_note (pitch, low, high): # function to check if a note is not forbidden

        if pitch in forbidden_notes:
            if abs(pitch - low) < abs(pitch - high):
                return pitch + 1 #value closer to low limit so + value
            else:
                return pitch - 1 #value closer to low limit so - value
        else: 
            return pitch #return value as it was
    
    def scale (percentage, instrument): # scale notes

        # lower and upperbound
        flute_low = 79 #G5
        flute_high = 101 #F7
        violin_low = 72 #C5
        violin_high = 96 #C7
        piano_low = 72 #C5
        piano_high = 84 #C6
        guitar_low = 55 #G3
        guitar_high = 67 #G4
        saxophone_low = 84 #C6
        saxophone_high = 96 #C7

        match instrument:
            case 'flute':
                return forbidden_note (((percentage/100) * (flute_high - flute_low) + flute_low), flute_low, flute_high) # check if note is forbidden or not
            case 'violin':
                return forbidden_note (((percentage/100) * (violin_high - violin_low) + violin_low), violin_low, violin_high) # check if note is forbidden or not
            case 'piano':
                return forbidden_note (((percentage/100) * (piano_high - piano_low) + piano_low), piano_low, piano_high) # check if note is forbidden or not
            case 'guitar':
                return forbidden_note (((percentage/100) * (guitar_high - guitar_low) + guitar_low), guitar_low, guitar_high) # check if note is forbidden or not
            case 'saxophone':
                return forbidden_note (((percentage/100) * (saxophone_high - saxophone_low) + saxophone_low), saxophone_low, saxophone_high) # check if note is forbidden or not

    def piano_notes (input_note, note_1, note_2, note_3): # sclae note for guitar
        match input_note:
            case 72: #C5
                note_1 = 72 #C5
                note_2 = 69 #A4 
                note_3 = 65 #F4
            case 74: #D5
                note_1 = 74 #D5 
                note_2 = 71 #B4 
                note_3 = 67 #G4
            case 76: #E5
                note_1 = 76 #E5 
                note_2 = 72 #C5
                note_3 = 69 #A4
            case 77: #F5
                note_1 = 77 #F5 
                note_2 = 74 #D5
                note_3 = 70 #A#4
            case 79: #G5
                note_1 = 79 #G5 
                note_2 = 76 #E5
                note_3 = 72 #C5
            case 81: #A5
                note_1 = 81 #A5 
                note_2 = 77 #F5
                note_3 = 74 #D5
            case 83: #B4
                note_1 = 83 #B4 
                note_2 = 79 #G5
                note_3 = 76 #E5

        return note_1, note_2, note_3 

    # --- declare variables
    model_custom_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files') #path of the audio files save location
    amount_of_instruments = len(list) # number of object on the screen  
    iteration = 0 # used to go over all the shapes in the pictures   
    
    # define variables amount and objects
    # --- high --- single
    amount_of_flute = 0 
    object_flute = 0    
    amount_of_violin = 0 # could also be mid
    object_violin = 0 # could also be mid    
    # --- mid --- accord
    amount_of_guitar = 0    
    object_guitar = 0
    amount_of_piano = 0
    object_piano = 0
    # --- low --- single 
    amount_of_drum = 0    
    object_drum = 0
    amount_of_saxophone = 0  
    object_saxophone = 0
    # --- kick --- single
    amount_of_kick = 0
    object_kick = 0
    # --- clap --- single
    amount_of_clap = 0    
    object_clap = 0
    # --- bpm ---
    bpm = 0
    
    forbidden_notes = [22,25,27,30,32,34,42,44,46,49,51,54,56,58,61,63,66,68,70,73,75,78,80,82,85,87,90,92,94,97,99,102,104,106]
    
    # determine the amount of shapes with the same instrument in the list
    for shape in list:
        match shape.instrument:
            case 'flute':   
                amount_of_flute += 1
                bpm = bpm + shape.bpm 
            case 'violin':  
                amount_of_violin += 1
                bpm = bpm + shape.bpm 
            case 'guitar':  
                amount_of_guitar += 1
                bpm = bpm + shape.bpm    
            case 'piano':   
                amount_of_piano += 1
                bpm = bpm + shape.bpm 
            case 'drum':  
                amount_of_drum += 1
                bpm = bpm + shape.bpm 
            case 'saxophone':  
                amount_of_saxophone += 1
                bpm = bpm + shape.bpm 
            case 'kick':  
                amount_of_kick += 1
                bpm = bpm + shape.bpm 
            case 'clap':   
                amount_of_clap += 1
                bpm = bpm + shape.bpm 
            
            case _: pass        

    bpm = bpm/amount_of_instruments # determen bpm of composition

    # make midi file for every instrument
    midi_flute          = MIDIFile(amount_of_flute,     removeDuplicates=False) # high
    midi_violin         = MIDIFile(amount_of_violin,    removeDuplicates=False) # high 
    midi_guitar         = MIDIFile(amount_of_guitar,    removeDuplicates=False) # mid
    midi_piano          = MIDIFile(amount_of_piano,     removeDuplicates=False) # mid
    midi_drum           = MIDIFile(amount_of_drum,      removeDuplicates=False) # low     
    midi_saxophone      = MIDIFile(amount_of_saxophone, removeDuplicates=False) # low     
    midi_kick           = MIDIFile(amount_of_kick,      removeDuplicates=False) # kick
    midi_clap           = MIDIFile(amount_of_clap,      removeDuplicates=False) # clap
    
    # -----------flute / high-----------
    # add tracks
    time_flute = 0 # time to zero
    channel_flute = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_flute.addTrackName(object_flute, time_flute, f"Track{object_flute}") # give track a name
    midi_flute.addTempo(object_flute, time_flute, bpm) # set bpm
    midi_flute.addProgramChange(object_flute, 0, time_flute, 1) # add instrument = shape.instrument = 1

    # -----------violin / high-----------
    # add tracks
    time_violin = 0 # time to zero
    channel_violin = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_flute.addTrackName(object_violin, time_violin, f"Track{object_violin}") # give track a name
    midi_flute.addTempo(object_violin, time_violin, bpm) # set bpm
    midi_flute.addProgramChange(object_violin, 0, time_violin, 1) # add instrument = shape.instrument = 1

    # -----------guitar / mid-----------
    # add tracks
    time_guitar = 0 # time to zero
    channel_guitar = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_guitar.addTrackName(object_guitar, time_guitar, f"Track{object_guitar}") # give track a name
    midi_guitar.addTempo(object_guitar, time_guitar, bpm) # set bpm
    midi_guitar.addProgramChange(object_guitar, 0, time_guitar, 1) # add instrument = shape.instrument = 1

    # -----------piano / mid-----------
    # add tracks
    time_piano = 0 # time to zero
    channel_piano = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_piano.addTrackName(object_piano, time_piano, f"Track{object_piano}") # give track a name
    midi_piano.addTempo(object_piano, time_piano, bpm) # set bpm
    midi_piano.addProgramChange(object_piano, 0, time_piano, 1) # add instrument = shape.instrument = 1

    # -----------drum / low-----------
    # add tracks
    time_drum = 0 # time to zero
    channel_drum = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_drum.addTrackName(object_drum, time_drum, f"Track{object_drum}") # give track a name
    midi_drum.addTempo(object_drum, time_drum, bpm) # set bpm
    midi_drum.addProgramChange(object_drum, 0, time_drum, 1) # add instrument = shape.instrument = 1

    # -----------saxophone / low-----------
    # add tracks
    time_saxophone = 0 # time to zero
    channel_saxophone = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_saxophone.addTrackName(object_saxophone, time_saxophone, f"Track{object_saxophone}") # give track a name
    midi_saxophone.addTempo(object_saxophone, time_saxophone, bpm) # set bpm
    midi_saxophone.addProgramChange(object_saxophone, 0, time_saxophone, 1) # add instrument = shape.instrument = 1

    # -----------kick-----------
    # add tracks
    time_kick = 0 # time to zero
    channel_kick = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_kick.addTrackName(object_kick, time_kick, f"Track{object_kick}") # give track a name
    midi_kick.addTempo(object_kick, time_kick, bpm) # set bpm
    midi_kick.addProgramChange(object_kick, 0, time_kick, 1) # add instrument = shape.instrument = 1

    # -----------clap-----------
    # add tracks
    time_clap = 0 # time to zero
    channel_clap = 0 #channel to zero
    # create ass many tracks as objects on the board    
    midi_clap.addTrackName(object_clap, time_clap, f"Track{object_clap}") # give track a name
    midi_clap.addTempo(object_clap, time_clap, bpm) # set bpm
    midi_clap.addProgramChange(object_clap, 0, time_clap, 1) # add instrument = shape.instrument = 1
    
    #fill midi files with notes
    for shape in list:
        
        #add flute notes
        if amount_of_flute > 0 and shape.instrument == "flute":
            
            midi_flute.addNote(object_flute, channel_flute, scale(shape.pitch, "flute"), shape.note_placement, 1, shape.volume) # add a note

            object_drum +=1

        #add violin notes
        if amount_of_violin > 0 and shape.instrument == "violin":

            midi_violin.addNote(object_violin, channel_violin, scale(shape.pitch, "violin"), shape.note_placement, 1, shape.volume) # add a note

            object_violin += 1

        #add guitar notes
        if amount_of_guitar > 0 and shape.instrument == "guitar":
            
            midi_guitar.addNote(object_guitar, channel_guitar, scale(shape.pitch, "guitar"), shape.note_placement, 1, shape.volume) # add a note

            object_guitar += 1

        #add piano notes
        if amount_of_piano > 0 and shape.instrument == "piano":
            
            
            piano_pitch_note_1, piano_pitch_note_2, piano_pitch_note_3 = piano_notes(scale(shape.pitch, "piano"))

            # add an accord
            midi_piano.addNote(object_piano, channel_piano, piano_pitch_note_1, shape.note_placement, 1, shape.volume) # add a note
            midi_piano.addNote(object_piano, channel_piano, piano_pitch_note_2, shape.note_placement, 1, shape.volume) # add a note
            midi_piano.addNote(object_piano, channel_piano, piano_pitch_note_3, shape.note_placement, 1, shape.volume) # add a note

            object_piano += 1

        #add drum notes
        if amount_of_drum > 0 and shape.instrument == "drum":
            
            midi_drum.addNote(object_drum, channel_drum, 84, shape.note_placement, 1, shape.volume) # add a note

            object_drum +=1

        #add saxophone notes
        if amount_of_saxophone > 0 and shape.instrument == "saxophone":
            
            midi_saxophone.addNote(object_saxophone, channel_saxophone, scale(shape.pitch, "saxophone"), shape.note_placement, 1, shape.volume) # add a note

            object_saxophone +=1

        #add kick notes
        if amount_of_kick > 0 and shape.instrument == "kick":
            
            midi_kick.addNote(object_kick, channel_kick, 84, shape.note_placement, 1, shape.volume) # add a note

            object_kick +=1
        
        #add clap notes
        if amount_of_clap > 0 and shape.instrument == "clap":
        
            midi_clap.addNote(object_clap, channel_clap, 84, shape.note_placement, 1, shape.volume) # add a note

            object_clap +=1
        
        #Mmake wav files of all the midi's when al nodes are added
        if amount_of_instruments -1 == iteration:
            if amount_of_flute == 0:
                midi_flute.addNote(object_flute, channel_flute, 0, 0, 0, 0) #clear track
            if amount_of_violin == 0:
                midi_violin.addNote(object_violin, channel_violin, 0, 0, 0, 0) #clear track 
            if amount_of_guitar == 0:
                midi_guitar.addNote(object_guitar, channel_guitar, 0, 0, 0, 0) #clear track
            if amount_of_piano == 0:
                midi_piano.addNote(object_piano, channel_piano, 0, 0, 0, 0) #clear track
            if amount_of_drum == 0:
                midi_drum.addNote(object_drum, channel_drum, 0, 0, 0, 0) #clear track 
            if amount_of_saxophone == 0:
                midi_saxophone.addNote(object_saxophone, channel_saxophone, 0, 0, 0, 0) #clear track
            if amount_of_kick == 0:
                midi_kick.addNote(object_kick, channel_kick, 0, 0, 0, 0) #clear track
            if amount_of_clap == 0:
                midi_clap.addNote(object_clap, channel_clap, 0, 0, 0, 0) #clear track

            #write all the midi files
            with open(model_custom_path + "\\flute_output.mid", "wb") as output_file1: 
                midi_flute.writeFile(output_file1)
            with open(model_custom_path + "\\violin_output.mid", "wb") as output_file2:
                midi_violin.writeFile(output_file2)
            with open(model_custom_path + "\\piano_output.mid", "wb") as output_file3:
                midi_guitar.writeFile(output_file3)
            with open(model_custom_path + "\\guitar_output.mid", "wb") as output_file4:
                midi_violin.writeFile(output_file4)
            with open(model_custom_path + "\\drum_output.mid", "wb") as output_file5:
                midi_drum.writeFile(output_file5)
            with open(model_custom_path + "\\saxophone_output.mid", "wb") as output_file6: 
                midi_saxophone.writeFile(output_file6)
            with open(model_custom_path + "\\kick_output.mid", "wb") as output_file7:
                midi_kick.writeFile(output_file7)
            with open(model_custom_path + "\\clap_output.mid", "wb") as output_file8:
                midi_clap.writeFile(output_file8)

        iteration += 1

    

