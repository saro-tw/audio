import pyaudio
import numpy as np

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BLOCK_SIZE = 1024
THRESHOLD = 0.999

# Initialize PyAudio
pa = pyaudio.PyAudio()

# Open the audio stream
stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=BLOCK_SIZE)

# Main loop
history = np.zeros((RATE // BLOCK_SIZE, BLOCK_SIZE // 2))
ptr = 0

while True:
    # Read audio data from the stream
    data = stream.read(BLOCK_SIZE)
    samples = np.frombuffer(data, dtype=np.int16)
    samples = samples.astype(np.float32) / 32768.0
    
    # Compute the short-time Fourier transform of the audio data
    spec = np.abs(np.fft.rfft(samples))
    
    # Compute the cross-correlation between the current spectrum and the history
    corr = np.abs(np.fft.irfft(spec * history[ptr]))
    
    # Check if the correlation is above the threshold
    if np.max(corr) > THRESHOLD:
        print('Audio is repeating!')
    
    # Update the history buffer
    history[ptr] = spec
    ptr = (ptr + 1) % history.shape[0]
