import numpy as np
import wave
import pyaudio

Chunk=1024
Format = pyaudio.paInt16
Rate = 44100
seconds = 3

Channels = 1

p = pyaudio.PyAudio( )
stream = p.open(format=Format,
              channels=Channels,
              rate=Rate,
              input=True,
              frames_per_buffer=Chunk)
print("start opnemen")
frames = []
for i in range(0,int(Rate/Chunk*seconds)):
    data = stream.read(Chunk)
    frames.append(data)
print("opnemen gestopt")
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("test.wav", 'wb')
wf.setnchannels(Channels)
wf.setsampwidth(p.get_sample_size(Format))
wf.setframerate(Rate)
wf.writeframes(b''.join(frames))
wf.close

chunk = 1024
rate = 44100
db_drop= 20
results = []
files = []

def bereken_dB(wav_file):
    wf = wave.open(wav_file, 'rb')
    data = wf.readframes(wf.getnframes())
    wf.close()
    
    audio_signal = np.abs(np.frombuffer(data, dtype="int16"))
    ref = 2**15 
    dB = 20 * np.log10(audio_signal[audio_signal > 0]/ref)
    
    return dB

def twintig_dB_drop(wav_file, target_drop_dB):
    dB = bereken_dB(wav_file)
   
    max_dB = np.max(dB)
    imax_dB = np.argmax(dB)


    drop_index = np.argmax(dB[imax_dB:] <= (max_dB - 3 * db_drop))
    time_of_drop = np.round((drop_index * chunk / rate), decimals=3)

    return time_of_drop

file = r"C:\Users\leoni\Downloads\test.wav"
time_of_drop = twintig_dB_drop(file, db_drop)
results.append(time_of_drop)
files.append(file)

print(results)
