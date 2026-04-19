# 🎵 Project [25201] Evaluating Perceptual Audio Encoding Performance

AudioEncode is an interactive tool developed in Python and Streamlit designed to evaluate the performance of audio compression algorithms. The system analyzes the trade-off between compression efficiency and signal quality using quantitative metrics and spectral analysis.

---

## Key Features

* **Multi-Level Encoding:** Supports MP3 compression at bitrates of 32, 64, 128, and 320 kbps using FFmpeg (LAME encoder).
* **Automatic Signal Alignment:** Implements an optimized FFT-based cross-correlation algorithm to align original and compressed signals, compensating for encoder delay with $O(N \log N)$ complexity.
* **Objective Quality Metrics:**
  * **Signal-to-Noise Ratio (SNR):** Mathematical signal fidelity.
  * **Processing Latency:** Real-time encoding duration (in seconds).
  * **Bitrate Estimation:** Based on compressed file size and signal duration.
  * **Compression Ratio:** Storage efficiency index.
* **Perceptual Evaluation:**
  * **STOI (Short-Time Objective Intelligibility):** Optimized for speech signals.
  * **Spectral Cosine Similarity:** Computed on STFT magnitude for music signals.
* **Visualization:** Comparison of Waveforms and Spectrograms.

---

## 📂 Project Structure

```text
├── app.py
├── config
│   ├── music_orchestra.yaml
│   └── speech_male.yaml
├── data
│   ├── Download_data.py
│   ├── encode
│   └── raw
│       ├── music
│       ├── speech
│       └── uploads
├── packages.txt
├── README.md
├── requirements.txt
├── results
│   ├── spectrogram
│   └── waveform
└── src
    ├── encoder.py
    ├── __init__.py
    ├── metrics.py
    └── visualization.py
```

---

## 📥 Data Acquisition

Before running the application, you need `.wav` files in the `data/raw/` directory. You can obtain these audio samples using one of the following methods:

**Method 1: Automated Download**
Run the provided script to automatically fetch built-in sample `.wav` files directly into your workspace:
```bash
python data/Download_data.py
```

**Method 2: Manual Download**
You can manually download standard `.wav` audio samples from the following open-source repositories and place them into the `data/raw/` folder:
* [SampleLib - Free WAV Audio Samples](https://samplelib.com/sample-wav.html)
* [File Examples - Sample Audio Files](https://file-examples.com/index.php/sample-audio-files/sample-wav-download/)

---
## Installation & Setup

```bash
git clone https://github.com/HuyennTran/AudioEncode.git
cd AudioEncode
pip install -r requirements.txt
```

### Install FFmpeg (required)

* Ubuntu:

```bash
sudo apt install ffmpeg
```

* Windows:
  Download from https://ffmpeg.org and add to PATH

---

## Run the Application

```bash
streamlit run app.py
```

---

## Evaluation Details

### 1. Signal Alignment

Signals are aligned using cross-correlation to compensate for encoder delay before computing metrics.

### 2. Metrics

* **Signal-to-Noise Ratio (SNR):**
  Measures distortion between original and compressed signals.

* **Bitrate:**
  Estimated from compressed file size and signal duration.

* **Compression Ratio:**
  Ratio between original file size and compressed file size.

### 3. Perceptual Metrics

* **Speech Mode:**

  * STOI (Short-Time Objective Intelligibility)

* **Music Mode:**

  * Spectral Cosine Similarity computed on STFT magnitude

---

## Visualization

The system provides:

* Waveform comparison (original vs compressed)
* Spectrogram comparison 
---

## Notes

* Input format should be `.wav` for original signals.
* FFmpeg must be installed for encoding to work properly.

---

## Future Work

* Improve perceptual metrics for music signals
* Integrate advanced codecs (e.g., neural audio codecs)
* Add additional evaluation metrics 
---

