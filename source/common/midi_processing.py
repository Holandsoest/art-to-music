import dawdreamer as daw
from scipy.io import wavfile
from pydub import AudioSegment
import os

sample_rate = 44100
buffer_size = 128
render_time = 4
model_midi_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
model_preset_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'preset_files')
model_wav_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'wav_files')
model_plugin_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'StupidSimpleSampler')      

def drum(list_of_objects, amount_of_drum):
    for shape in list_of_objects:
        if amount_of_drum == 0:
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", model_plugin_path + "\\StupidSimpleSampler.dll")
            assert synth.get_name() == "my_synth"
            synth.load_state(model_preset_path + "\\kick.fxb")
            synth.open_editor()
            synth.load_midi(model_midi_path + "\\drum_output.mid", clear_previous=False, beats=False, all_events=False) 
            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(model_wav_path + "\\drum.wav",  sample_rate, audio.transpose()) 
            amount_of_drum +=1

def guitar(list_of_objects, amount_of_guitar):      
    for shape in list_of_objects:  
        if amount_of_guitar == 0:
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", model_plugin_path + "\\StupidSimpleSampler.dll")
            assert synth.get_name() == "my_synth"
            synth.load_state(model_preset_path + "\\guitar.fxb")
            synth.load_midi(model_midi_path + "\\guitar_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(model_wav_path + "\\guitar.wav",  sample_rate, audio.transpose()) 
            amount_of_guitar +=1

def violin (list_of_objects, amount_of_violin):
    for shape in list_of_objects:
        if amount_of_violin == 0:
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", model_plugin_path + "\\StupidSimpleSampler.dll")
            assert synth.get_name() == "my_synth"
            synth.load_state(model_preset_path + "\\violin.fxb")
            synth.load_midi(model_midi_path + "\\violin_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(model_wav_path + "\\violin.wav",  sample_rate, audio.transpose()) 
            amount_of_violin +=1

def flute (list_of_objects, amount_of_flute):
    for shape in list_of_objects:
        if amount_of_flute == 0:
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", model_plugin_path + "\\StupidSimpleSampler.dll")
            assert synth.get_name() == "my_synth"
            synth.load_state(model_preset_path + "\\flute.fxb")
            synth.load_midi(model_midi_path + "\\flute_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(model_wav_path + "\\flute.wav",  sample_rate, audio.transpose())
            amount_of_flute +=1
            
def piano (list_of_objects, amount_of_piano):
    for shape in list_of_objects:
        if amount_of_piano == 0:
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", model_plugin_path + "\\StupidSimpleSampler.dll")
            assert synth.get_name() == "my_synth"
            synth.load_state(model_preset_path + "\\piano.fxb")
            #synth.open_editor()
            synth.load_midi(model_midi_path + "\\piano_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(model_wav_path + "\\piano.wav", sample_rate, audio.transpose())
            amount_of_piano +=1
    
def saxophone (list_of_objects, amount_of_saxophone):
    for shape in list_of_objects:
        if amount_of_saxophone == 0:
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", model_plugin_path + "\\StupidSimpleSampler.dll")
            assert synth.get_name() == "my_synth"
            synth.load_state(model_preset_path + "\\saxophone.fxb")
            synth.load_midi(model_midi_path + "\\saxophone_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(model_wav_path + "\\saxophone.wav", sample_rate, audio.transpose())
            amount_of_saxophone +=1
    
def clap (list_of_objects, amount_of_clap):
    for shape in list_of_objects:
        if amount_of_clap == 0:
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", model_plugin_path + "\\StupidSimpleSampler.dll")
            assert synth.get_name() == "my_synth"
            synth.load_state(model_preset_path + "\\clap.fxb")
            synth.load_midi(model_midi_path + "\\clap_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(model_wav_path + "\\clap.wav", sample_rate, audio.transpose())
            amount_of_clap +=1

def audio_rendering():
    # Load the first MP3 file
    sound1 = AudioSegment.from_file(model_wav_path + "\\drum.wav", format="wav")
    sound2 = AudioSegment.from_file(model_wav_path + "\\flute.wav", format="wav")
    sound3 = AudioSegment.from_file(model_wav_path + "\\violin.wav", format="wav")
    sound4 = AudioSegment.from_file(model_wav_path + "\\clap.wav", format="wav")
    sound5 = AudioSegment.from_file(model_wav_path + "\\saxophone.wav", format="wav")
    sound6 = AudioSegment.from_file(model_wav_path + "\\guitar.wav", format="wav")
    sound7 = AudioSegment.from_file(model_wav_path + "\\piano.wav", format="wav")

    # Set the desired overlap time in milliseconds
    overlap_time = render_time * 1000

    # Extract the overlapping part from the end of the first MP3 file
    overlap_part = sound1[-overlap_time:]
    overlap_part1 = sound2[-overlap_time:]
    overlap_part2 = sound3[-overlap_time:]
    overlap_part3 = sound4[-overlap_time:]
    overlap_part4 = sound5[-overlap_time:]
    overlap_part5 = sound6[-overlap_time:]
    
    # Combine the overlapping part of the first MP3 file with the second MP3 file
    combined_sound = overlap_part.overlay(sound7)
    combined_sound2 = overlap_part1.overlay(combined_sound)
    combined_sound3 = overlap_part2.overlay(combined_sound2)
    combined_sound4 = overlap_part3.overlay(combined_sound3)
    combined_sound5 = overlap_part4.overlay(combined_sound4)
    combined_sound6 = overlap_part5.overlay(combined_sound5)

    # Export the combined audio to an MP3 file
    with open("files\\audio_generator\\created_song.mp3", "wb") as output_file1:
                combined_sound6.export(output_file1, format = "mp3")

