import dawdreamer as daw
from scipy.io import wavfile
from pydub import AudioSegment
import os
import multiprocessing as mp

def AudiRenderPlugin(list):
    sample_rate = 44100
    buffer_size = 128
    render_time = 6
    amount_of_drum = 0
    amount_of_guitar = 0
    amount_of_violin = 0
    amount_of_flute = 0
    amount_of_cello = 0
    
    AudioSegment.ffmpeg 

    model_midi_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
    model_preset_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'preset_files')
    model_wav_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'wav_files')

    for shape in list:
            match shape.instrument:
                case 'drum':    amount_of_drum = 1
                case 'guitar':  amount_of_guitar = 1
                case 'violin':  amount_of_violin = 1
                case 'flute':   amount_of_flute = 1
                case 'cello':   amount_of_cello = 1
                case _: pass  

    def drum(list_of_objects, drum):
        for shape in list_of_objects:
            if drum == 1:
                engine = daw.RenderEngine(sample_rate, buffer_size)
                synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
                assert synth.get_name() == "my_synth"
                synth.load_state(model_preset_path + "\\drum_preset")
                synth.load_midi(model_midi_path + "\\drum_output.mid", clear_previous=False, beats=False, all_events=False) 
                engine.load_graph([
                                (synth,[])
                ])
                engine.set_bpm(shape.bpm)
                engine.render(render_time)  
                audio = engine.get_audio()  
                wavfile.write(model_wav_path + "\\drum.wav",  sample_rate, audio.transpose()) 
                drum +=1
                print("drum")

    def guitar(list_of_objects, guitar):      
        for shape in list_of_objects:
            if guitar == 1:
                engine = daw.RenderEngine(sample_rate, buffer_size)
                synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
                assert synth.get_name() == "my_synth"
                synth.load_state(model_preset_path + "\\guitar_preset")
                synth.load_midi(model_midi_path + "\\guitar_output.mid", clear_previous=False, beats=False, all_events=False) 

                engine.load_graph([
                                (synth,[])
                ])
                engine.set_bpm(shape.bpm)
                engine.render(render_time)  
                audio = engine.get_audio()  
                wavfile.write(model_wav_path + "\\guitar.wav",  sample_rate, audio.transpose()) 
                guitar +=1
                print("guitar")

    def violin (list_of_objects, violin):
        for shape in list_of_objects:
            if violin == 1:
                engine = daw.RenderEngine(sample_rate, buffer_size)
                synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
                assert synth.get_name() == "my_synth"
                synth.load_state(model_preset_path + "\\violin_preset")
                synth.load_midi(model_midi_path + "\\violin_output.mid", clear_previous=False, beats=False, all_events=False) 

                engine.load_graph([
                                (synth,[])
                ])
                engine.set_bpm(shape.bpm)
                engine.render(render_time)  
                audio = engine.get_audio()  
                wavfile.write(model_wav_path + "\\violin.wav",  sample_rate, audio.transpose())
                violin +=1
                print("violin")

    def flute (list_of_objects, flute):
        for shape in list_of_objects:
            if flute == 1:
                engine = daw.RenderEngine(sample_rate, buffer_size)
                synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
                assert synth.get_name() == "my_synth"
                synth.load_state(model_preset_path + "\\flute_preset")
                synth.load_midi(model_midi_path + "\\flute_output.mid", clear_previous=False, beats=False, all_events=False) 

                engine.load_graph([
                                (synth,[])
                ])
                engine.set_bpm(shape.bpm)
                engine.render(render_time)  
                audio = engine.get_audio()  
                wavfile.write(model_wav_path + "\\flute.wav",  sample_rate, audio.transpose())
                flute +=1
                print("flute")
                
    def cello (list_of_objects, cello):
        for shape in list_of_objects:
            if cello == 1:
                engine = daw.RenderEngine(sample_rate, buffer_size)
                synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
                assert synth.get_name() == "my_synth"
                synth.load_state(model_preset_path + "\\cello_preset")
                synth.load_midi(model_midi_path + "\\cello_output.mid", clear_previous=False, beats=False, all_events=False) 

                engine.load_graph([
                                (synth,[])
                ])
                engine.set_bpm(shape.bpm)
                engine.render(render_time)  
                audio = engine.get_audio()  
                wavfile.write(model_wav_path + "\\cello.wav", sample_rate, audio.transpose())
                cello +=1
                print("cello")
                
    p1 = mp.Process(target=drum, args=(list, amount_of_drum))
    p2 = mp.Process(target=violin, args=(list, amount_of_violin))
    p3 = mp.Process(target=guitar, args=(list, amount_of_guitar))
    p4 = mp.Process(target=flute, args=(list, amount_of_flute))
    p5 = mp.Process(target=cello, args=(list, amount_of_cello))

    if __name__ == "__main__":
        print(1)   
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()         

    # Load the first MP3 file
    sound1 = AudioSegment.from_file(model_wav_path + "\\drum.wav", format="wav")
    sound2 = AudioSegment.from_file(model_wav_path + "\\flute.wav", format="wav")
    sound3 = AudioSegment.from_file(model_wav_path + "\\violin.wav", format="wav")
    sound4 = AudioSegment.from_file(model_wav_path + "\\cello.wav", format="wav")
    sound5 = AudioSegment.from_file(model_wav_path + "\\guitar.wav", format="wav")

    # Set the desired overlap time in milliseconds
    overlap_time = render_time * 1000

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
    with open("files\\audio_generator\\created_song.mp3", "wb") as output_file1:
                combined_sound4.export(output_file1, format = "mp3")
