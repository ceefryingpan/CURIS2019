import librosa
import numpy as np
import scipy.io.wavfile.read as reader

sr, y = reader('\Users\jksla\Downloads\gates.wav')
# y, sr = librosa.load('\Users\jksla\Downloads\gates.wav', sr = 16000)
spec = np.log10(np.abs((lobrosa.stft(y, 512, 160, 512))))