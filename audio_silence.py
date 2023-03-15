import pyaudio
import numpy as np

# Define constants
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

# Define a function to analyze the audio stream for dropouts
def detect_dropouts(stream):
    while True:
        # Read a chunk of audio data
        data = stream.read(CHUNK_SIZE)
        
        # Convert the data to a NumPy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Check if the audio data contains zeros
        if np.any(audio_data == 0):
            print("Dropout detected!")
            
# Call the detect_dropouts function to start analyzing the stream
detect_dropouts(stream)
