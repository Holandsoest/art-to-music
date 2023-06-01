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
                return forbidden_note (int(((percentage/100) * (flute_high - flute_low) + flute_low)), flute_low, flute_high) # check if note is forbidden or not
            case 'violin':
                return forbidden_note (int(((percentage/100) * (violin_high - violin_low) + violin_low)), violin_low, violin_high) # check if note is forbidden or not
            case 'piano':
                return forbidden_note (int(((percentage/100) * (piano_high - piano_low) + piano_low)), piano_low, piano_high) # check if note is forbidden or not
            case 'guitar':
                return forbidden_note (int(((percentage/100) * (guitar_high - guitar_low) + guitar_low)), guitar_low, guitar_high) # check if note is forbidden or not
            case 'saxophone':
                return forbidden_note (int(((percentage/100) * (saxophone_high - saxophone_low) + saxophone_low)), saxophone_low, saxophone_high) # check if note is forbidden or not

    def piano_notes (input_note): # sclae note for guitar
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
            case _: pass

        return [note_1, note_2, note_3]

    # --- declare variables
    model_custom_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files') #path of the audio files save location
    amount_of_instruments = len(list) # number of object on the screen  
    iteration = 0 # used to go over all the shapes in the pictures   
    
    # define variables amount and objects
    # --- high --- single
    amount_of_flute = 0 
    amount_of_violin = 0 # could also be mid

    # --- mid --- accord
    amount_of_guitar = 0    
    amount_of_piano = 0
 
    # --- low --- single 
    amount_of_drum = 0    
    amount_of_saxophone = 0

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
            case _: pass        

    bpm = int(bpm/amount_of_instruments) # determen bpm of composition

    # make midi file for every instrument
    midi_flute          = MIDIFile(1, removeDuplicates=False) # high
    midi_violin         = MIDIFile(1, removeDuplicates=False) # high 
    midi_guitar         = MIDIFile(1, removeDuplicates=False) # mid
    midi_piano          = MIDIFile(1, removeDuplicates=False) # mid
    midi_drum           = MIDIFile(1, removeDuplicates=False) # low     
    midi_saxophone      = MIDIFile(1, removeDuplicates=False) # low     
    midi_clap           = MIDIFile(1, removeDuplicates=False) # clap
    
    # -----------flute / high-----------  
    midi_flute.addTrackName(0, 0, "Track 0") # give track a name
    midi_flute.addTempo(0, 0, bpm) # set bpm
    midi_flute.addProgramChange(0, 0, 0, 1) # add instrument = shape.instrument = 1

    # -----------violin / high-----------
    midi_violin.addTrackName(0, 0, "Track0") # give track a name
    midi_violin.addTempo(0, 0, bpm) # set bpm
    midi_violin.addProgramChange(0, 0, 0, 1) # add instrument = shape.instrument = 1

    # -----------guitar / mid-----------
    midi_guitar.addTrackName(0, 0, "Track0") # give track a name
    midi_guitar.addTempo(0, 0, bpm) # set bpm
    midi_guitar.addProgramChange(0, 0, 0, 1) # add instrument = shape.instrument = 1

    # -----------piano / mid-----------
    midi_piano.addTrackName(0, 0, "Track0") # give track a name
    midi_piano.addTempo(0, 0, bpm) # set bpm
    midi_piano.addProgramChange(0, 0, 0, 1) # add instrument = shape.instrument = 1

    # -----------drum / low-----------
    midi_drum.addTrackName(0, 0, "Track0") # give track a name
    midi_drum.addTempo(0, 0, bpm) # set bpm
    midi_drum.addProgramChange(0, 0, 0, 1) # add instrument = shape.instrument = 1

    # -----------saxophone / low----------- 
    midi_saxophone.addTrackName(0, 0,"Track0") # give track a name
    midi_saxophone.addTempo(0, 0, bpm) # set bpm
    midi_saxophone.addProgramChange(0, 0, 0, 1) # add instrument = shape.instrument = 1

    # -----------clap-----------
    midi_clap.addTrackName(0, 0, "Track0") # give track a name
    midi_clap.addTempo(0, 0, bpm) # set bpm
    midi_clap.addProgramChange(0, 0, 0, 1) # add instrument = shape.instrument = 1

    #fill midi files with notes
    for shape in list:
        #add flute notes
        if amount_of_flute > 0 and shape.instrument == "flute":
            midi_flute.addNote(0, 0, scale(shape.pitch, "flute"), shape.note_placement, 1, shape.volume) # add a note
        
        if amount_of_drum > 0 and shape.instrument == "drum":
            if amount_of_drum == 1 or 5 or 9 or 13:
                midi_drum.addNote(0, 0, 70, 0, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 2, 0.5, 120) # add a note

                midi_clap.addNote(0, 0, 70, 2, 0.5, 120) # add a note

            if amount_of_drum == 2 or 6 or 10 or 14:
                midi_drum.addNote(0, 0, 70, 0, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 2, 0.5, 120) # add a note
                
                midi_clap.addNote(0, 0, 70, 0.75, 0.5, 120) # add a note
                midi_clap.addNote(0, 0, 70, 3, 0.5, 120) # add a note
            
            if amount_of_drum == 3 or 7 or 11 or 15:
                midi_drum.addNote(0, 0, 70, 0, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 1, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 2, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 3, 0.5, 120) # add a note
                
                midi_clap.addNote(0, 0, 70, 1, 0.5, 120) # add a note
                midi_clap.addNote(0, 0, 70, 3, 0.5, 120) # add a note
            
            if amount_of_drum == 4 or 8 or 12:
                midi_drum.addNote(0, 0, 70, 0, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 1, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 2, 0.5, 120) # add a note
                midi_drum.addNote(0, 0, 70, 3, 0.5, 120) # add a note
                
                midi_clap.addNote(0, 0, 70, 1.5, 0.5, 120) # add a note
                midi_clap.addNote(0, 0, 70, 2.75, 0.5, 120) # add a note

        #add violin notes
        if amount_of_violin > 0 and shape.instrument == "violin":
            midi_violin.addNote(0, 0, scale(shape.pitch, "violin"), shape.note_placement, 1, shape.volume) # add a note

        #add guitar notes
        if amount_of_guitar > 0 and shape.instrument == "guitar":
            midi_guitar.addNote(0, 0, scale(shape.pitch, "guitar"), shape.note_placement, 0.5, shape.volume) # add a note


        #add piano notes
        if amount_of_piano > 0 and shape.instrument == "piano":
            notes = piano_notes(scale(shape.pitch, "piano"))

            # add an chord
            midi_piano.addNote(0, 0, notes[0], shape.note_placement, 1, shape.volume) # add a note
            midi_piano.addNote(0, 0, notes[1], shape.note_placement, 1, shape.volume) # add a note
            midi_piano.addNote(0, 0, notes[2], shape.note_placement, 1, shape.volume) # add a note

        #add saxophone notes
        if amount_of_saxophone > 0 and shape.instrument == "saxophone":
            midi_saxophone.addNote(0, 0, scale(shape.pitch, "saxophone"), shape.note_placement, 1, shape.volume) # add a note

        #Make wav files of all the midi's when al nodes are added
        if amount_of_instruments -1 == iteration:
            if amount_of_flute == 0:
                midi_flute.addNote(0, 0, 0, 1, 1, 120) #clear track
            if amount_of_violin == 0:
                midi_violin.addNote(0, 0, 0, 1, 1, 120) #clear track 
            if amount_of_guitar == 0:
                midi_guitar.addNote(0, 0, 0, 1, 1, 120) #clear track
            if amount_of_piano == 0:
                midi_piano.addNote(0, 0, 0, 1, 1, 120) #clear track
            if amount_of_saxophone == 0:
                midi_saxophone.addNote(0, 0, 0, 1, 1, 120) #clear track

            #write all the midi files
            with open(model_custom_path + "\\flute_output.mid", "wb") as output_file1: 
                midi_flute.writeFile(output_file1)
            with open(model_custom_path + "\\violin_output.mid", "wb") as output_file2:
                midi_violin.writeFile(output_file2)
            with open(model_custom_path + "\\guitar_output.mid", "wb") as output_file3:
                midi_guitar.writeFile(output_file3)
            with open(model_custom_path + "\\violin_output.mid", "wb") as output_file4:
                midi_violin.writeFile(output_file4)
            with open(model_custom_path + "\\drum_output.mid", "wb") as output_file5:
                midi_drum.writeFile(output_file5)
            with open(model_custom_path + "\\saxophone_output.mid", "wb") as output_file6: 
                midi_saxophone.writeFile(output_file6)
            with open(model_custom_path + "\\clap_output.mid", "wb") as output_file7:
                midi_clap.writeFile(output_file7)
            return bpm
        
        iteration += 1