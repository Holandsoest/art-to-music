import dawdreamer as daw
import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100
BUFFER_SIZE = 128

# extensions: .dll, .vst3, .vst, .component
# Make an engine. We'll only need one.
engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
#synth = engine.make_plugin_processor("my_synth", r"D:\Muziek\muziek\Fl studio plugins\Sylenth1\Sylenth1.dll")
assert synth.get_name() == "my_synth"
#synth.load_preset(r'D:\Muziek\muziek\Fl studio plugins\Sylenth1\Alex rome.fxp')

# For some plugins, it's possible to load presets:
#print(synth.get_parameters_description())
#synth.set_parameter("/MySine/freq", 440.)  # 440 Hz
synth.load_midi(r"C:\Users\gielw\Documents\Python\output1.mid", clear_previous=False, beats=False, all_events=False)

# Plugins can show their UI.
synth.open_editor()  # Open the editor, make changes, and close

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
wavfile.write('my_song2.wav', SAMPLE_RATE, audio.transpose()) # Don't forget to transpose!
# Render audio again!