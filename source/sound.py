import dawdreamer as daw
from scipy.io import wavfile
from pydub import AudioSegment

def AudiRenderPlugin(list):
    sample_rate = 44100
    buffer_size = 128
    render_time = 16
    amount_of_drum = 0
    amount_of_guitar = 0
    amount_of_flute = 0
    amount_of_violin = 0
    amount_of_cello = 0

    for shape in list:
        match shape.instrument:
            case 'drum':    amount_of_drum = 1
            case 'guitar':  amount_of_guitar = 1
            case 'flute':   amount_of_flute = 1
            case 'violin':  amount_of_violin = 1
            case 'cello':   amount_of_cello = 1
            case _: pass

    for shape in list:
        if amount_of_drum == 1 and shape.instrument == "drum":
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
            assert synth.get_name() == "my_synth"
            synth.load_state(f"files\daw_files\{shape.instrument}_preset")
            synth.load_midi(f"{shape.instrument}_output.mid", clear_previous=False, beats=False, all_events=False) 
            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(shape.instrument + '.wav', sample_rate, audio.transpose()) # Don't forget to transpose!
            amount_of_drum +=1
        
        if amount_of_guitar == 1 and shape.instrument == "guitar":
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
            assert synth.get_name() == "my_synth"
            synth.load_state(f"files\daw_files\{shape.instrument}_preset")
            synth.load_midi(f"{shape.instrument}_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(shape.instrument + '.wav', sample_rate, audio.transpose()) # Don't forget to transpose!
            amount_of_guitar +=1

        if amount_of_violin == 1 and shape.instrument == "violin":
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
            assert synth.get_name() == "my_synth"
            synth.load_state(f"files\daw_files\{shape.instrument}_preset")
            synth.load_midi(f"{shape.instrument}_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(shape.instrument + '.wav', sample_rate, audio.transpose()) # Don't forget to transpose!
            amount_of_violin +=1

        if amount_of_flute == 1 and shape.instrument == "flute":
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
            assert synth.get_name() == "my_synth"
            synth.load_state(f"files\daw_files\{shape.instrument}_preset")
            synth.load_midi(f"{shape.instrument}_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(shape.instrument + '.wav', sample_rate, audio.transpose()) # Don't forget to transpose!
            amount_of_flute +=1

        if amount_of_cello == 1 and shape.instrument == "cello":
            engine = daw.RenderEngine(sample_rate, buffer_size)
            synth = engine.make_plugin_processor("my_synth", r"C:\Program Files\Common Files\VST3\BBC Symphony Orchestra (64 Bit).vst3")
            assert synth.get_name() == "my_synth"
            synth.load_state(f"files\daw_files\{shape.instrument}_preset")
            synth.load_midi(f"{shape.instrument}_output.mid", clear_previous=False, beats=False, all_events=False) 

            engine.load_graph([
                            (synth,[])
            ])
            engine.set_bpm(shape.bpm)
            engine.render(render_time)  
            audio = engine.get_audio()  
            wavfile.write(shape.instrument + '.wav', sample_rate, audio.transpose()) # Don't forget to transpose!
            amount_of_cello +=1
   

    # Load the first MP3 file
    sound1 = AudioSegment.from_file("flute.wav", format="wav")
    sound2 = AudioSegment.from_file("drum.wav", format="wav")
    sound3 = AudioSegment.from_file("violin.wav", format="wav")
    sound4 = AudioSegment.from_file("cello.wav", format="wav")
    sound5 = AudioSegment.from_file("guitar.wav", format="wav")

    # Set the desired overlap time in milliseconds
    overlap_time = 16000

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