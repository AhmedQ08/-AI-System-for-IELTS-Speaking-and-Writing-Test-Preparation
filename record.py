import pyaudio
import wave

# Set parameters for the audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "./static/audio/user_audio.wav"

# Initialize variables
frames = []
recording = False
stream = None
audio = None
# Function to start recording
def start_recording():
    global frames, recording, stream, audio
    recording = True
    frames = []
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

# Function to stop recording
def stop_recording():
    global recording, stream, audio
    if recording:
        recording = False
        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        save_audio()

# Function to save the recorded audio to a WAV file
def save_audio():
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print("Audio saved as:", WAVE_OUTPUT_FILENAME)