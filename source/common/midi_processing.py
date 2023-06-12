import dawdreamer as daw
from scipy.io import wavfile
from pydub import AudioSegment
import os

sample_rate = 44100
buffer_size = 128
model_midi_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
model_preset_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'preset_files')
model_wav_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'wav_files')
model_plugin_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'StupidSimpleSampler')      

def instrument (bpm, instrument):
    engine = daw.RenderEngine(sample_rate, buffer_size)
    synth = engine.make_plugin_processor("my_synth", os.path.join(model_plugin_path, "StupidSimpleSampler.dll"))
    assert synth.get_name() == "my_synth"
    synth.load_state(os.path.join(model_preset_path, f"{instrument}.fxb"))
    synth.load_midi(os.path.join(model_midi_path, f"{instrument}_output.mid"), clear_previous=False, beats=False, all_events=False) 
    #synth.open_editor() #undo # to check if path from plugin is working
    engine.load_graph([
                    (synth,[])
    ])
    engine.set_bpm(bpm)
    engine.render(4/(bpm/60))  
    audio = engine.get_audio()  
    wavfile.write(os.path.join(model_wav_path, f"{instrument}.wav"),  sample_rate, audio.transpose())
       

def audio_rendering(bpm):
    AudioSegment.silent()
    # Load the MP3 files
    sound1 = AudioSegment.from_file(os.path.join(model_wav_path, "drum.wav"), format="wav")
    sound2 = AudioSegment.from_file(os.path.join(model_wav_path, "flute.wav"), format="wav")
    sound3 = AudioSegment.from_file(os.path.join(model_wav_path, "violin.wav"), format="wav")
    sound4 = AudioSegment.from_file(os.path.join(model_wav_path, "clap.wav"), format="wav")
    sound5 = AudioSegment.from_file(os.path.join(model_wav_path, "saxophone.wav"), format="wav")
    sound6 = AudioSegment.from_file(os.path.join(model_wav_path, "guitar.wav"), format="wav")
    sound7 = AudioSegment.from_file(os.path.join(model_wav_path, "piano.wav"), format="wav")

    # Set the desired overlap time in milliseconds
    overlap_time = 4/(bpm/60) * 1000

    # Extract the overlapping part from the end of the first MP3 file
    overlap_part = sound1[-overlap_time:]
    overlap_part1 = sound2[-overlap_time:]
    overlap_part2 = sound3[-overlap_time:]
    overlap_part3 = sound4[-overlap_time:]
    overlap_part4 = sound5[-overlap_time:]
    overlap_part5 = sound6[-overlap_time:]
    
    # Combine the overlapping part of the first MP3 file with the second MP3 file
    combined_sound = overlap_part.overlay(sound7)
    combined_sound1 = overlap_part1.overlay(combined_sound)
    combined_sound2 = overlap_part2.overlay(combined_sound1)
    combined_sound3 = overlap_part3.overlay(combined_sound2)
    combined_sound4 = overlap_part4.overlay(combined_sound3)
    combined_sound5 = overlap_part5.overlay(combined_sound4)

    combined_sound6 = (combined_sound5 + combined_sound5)*2
    # Export the combined audio to an MP3 file
    with open(os.path.join('files','audio_generator','created_song.mp3'), "wb") as output_file1:
                combined_sound6.export(output_file1, format = "mp3")
