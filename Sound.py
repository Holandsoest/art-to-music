import dawdreamer as daw
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

SAMPLE_RATE = 44100
BUFFER_SIZE = 128

# Make an engine. We'll only need one.
engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
#synth = engine.make_plugin_processor("my_synth", r"D:\Muziek\muziek\Fl studio plugins\Sylenth1\Sylenth1.dll")
assert synth.get_name() == "my_synth"
#synth.load_vst3_preset(r"C:\Users\gielw\Spitfire\Spitfire Audio - BBC Symphony Orchestra\Presets\v1.5.0\Discover Strings\BBCSODi_Violins 2_All.zpreset")
instrument = "cello"

synth.load_state(instrument + "_preset")

# For some plugins, it's possible to load presets:
#print(synth.get_parameters_description())
#synth.set_parameter("pitButton10")
#synth.set_parameter("/MySine/freq", 440.)  # 440 Hz.
synth.load_midi(r"MidiSound.mid", clear_previous=False, beats=False, all_events=False)

# Plugins can show their UI.
#synth.open_editor()  # Open the editor, make changes, and close

#synth.save_state("flute_preset")

engine.load_graph([
                   (synth, [])
])

# Load a MIDI file and keep the timing in units of beats. Changes to the Render Engine's BPM
# will affect the timing.

#print("synth num inputs: ", synth.get_num_input_channels())
#print("synth num outputs: ", synth.get_num_output_channels())

engine.set_bpm(120)
engine.render(10)  
audio = engine.get_audio()  
wavfile.write('cello.wav', SAMPLE_RATE, audio.transpose()) # Don't forget to transpose!

# Load the WAV file
SAMPLE_RATE1, audio = wavfile.read('my_song2.wav')

# Load the first MP3 file
sound1 = AudioSegment.from_file("flute.wav", format="wav")
sound2 = AudioSegment.from_file("drum.wav", format="wav")
sound3 = AudioSegment.from_file("violin.wav", format="wav")
sound4 = AudioSegment.from_file("cello.wav", format="wav")
sound5 = AudioSegment.from_file("guitar.wav", format="wav")

# Set the desired overlap time in milliseconds
overlap_time = 10000

# Extract the overlapping part from the end of the first MP3 file
overlap_part = sound1[-overlap_time:]
overlap_part1 = sound2[-overlap_time:]
overlap_part2 = sound3[-overlap_time:]
overlap_part3 = sound4[-overlap_time:]

# Combine the overlapping part of the first MP3 file with the second MP3 file
combined_sound = overlap_part.overlay(sound5)
combined_sound2 = overlap_part1.overlay(combined_sound)
combined_sound3 = overlap_part2.overlay(combined_sound2)
combined_sound4 = overlap_part3.overlay(combined_sound3)

# Export the combined audio to an MP3 file
combined_sound4.export("combined.mp3", format="mp3")