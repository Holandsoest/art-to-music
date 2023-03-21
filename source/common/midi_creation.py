from midiutil.MidiFile import MIDIFile
import pygame

def MakeSong(list):
    #pitch, bpm, duration, volume, instrument, amount
    amount_of_instruments = len(list)
    for shape in list:

        # create MIDIFile object
        midi = MIDIFile(amount_of_instruments, removeDuplicates=False)

        # add tracks
        track1 = 0
        time = 0
        channel = 0 
        instruments = 0

        while instruments < amount_of_instruments:
        # create ass many tracks as instruments        
            midi.addTrackName(instruments, time, f"Track{instruments}")
            midi.addTempo(instruments, time, shape.bpm)
            midi.addProgramChange(instruments, 0, time, shape.instrument)
            midi.addNote(track1, channel, shape.pitch, time, shape.duration, shape.volume)
            time = +2
            instruments +=1

        with open("output.mid", "wb") as output_file:
            midi.writeFile(output_file)
        
        pygame.mixer.init()
        #load MIDI file
        pygame.mixer.music.load("output.mid")
        # play MIDI file
        pygame.mixer.music.play()
        # wait for music to finish playing
        while pygame.mixer.music.get_busy():
            continue