import numpy as np
import os
from scipy.signal import correlate
from pystoi import stoi   

# align
def align_signals(x, y):
    corr = correlate(y, x)
    lag = np.argmax(corr) - len(x) + 1
    if lag > 0:
        y = y[lag:]
    else:
        x = x[-lag:]
    min_len = min(len(x), len(y))
    return x[:min_len], y[:min_len]
# SNR
def snr_db(x, y):
    x, y = align_signals(x, y)
    noise = x - y
    return 10 * np.log10(np.sum(x**2) / (np.sum(noise**2) + 1e-12))
# bittrate
def bitrate(file_path, signal, sr):
    size_bits = os.path.getsize(file_path) * 8
    duration = len(signal) / sr
    return size_bits / duration
# perceptual
def perceptual_score(x, y, sr):
    x, y = align_signals(x, y)
    return stoi(x, y, sr)