import streamlit as st
import os
import sys
import time

# Add the root directory to the system path to allow local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.encoder import encode_audio
from src.metrics import calculate_metrics
from src.visualization import plot_spectrogram_comparison, plot_waveform_comparison

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(page_title="Audio Codec Analyzer", layout="wide")
st.title("🎵 Project [25201] Evaluating Perceptual Audio Encoding Performance")

# ─────────────────────────────────────────────
# SIDEBAR — INPUT DATA
# ─────────────────────────────────────────────
st.sidebar.header("1. Input Audio")

# User chooses between built-in sample files or custom uploads
input_option = st.sidebar.radio("Data Source:", ["Use Sample File", "Upload Custom File (.wav)"])

# Define paths for storing encoded outputs and visualization results
output_dir = "data/encode"
img_dir    = "results"
raw_dir    = "data/raw/uploads"

# Ensure all required directories exist before processing
os.makedirs(output_dir, exist_ok=True)
os.makedirs(img_dir,    exist_ok=True)
os.makedirs(raw_dir,    exist_ok=True)

# Collect the list of audio files to process (up to 3)
original_files = []

if input_option == "Use Sample File":
    # Show files from both speech and music folders so mixed selection is possible
    all_sample_files = []
    for category in ["speech", "music"]:
        folder = f"data/raw/{category}"
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.endswith(".wav"):
                    # Store as (display_label, full_path) so the user sees the category
                    all_sample_files.append((f"{category}/{f}", os.path.join(folder, f)))

    if all_sample_files:
        labels = [item[0] for item in all_sample_files]
        selected_labels = st.sidebar.multiselect(
            "Select samples:",
            labels,
            max_selections=3,
            help="You can mix speech and music files"
        )
        # Resolve selected labels back to full file paths
        label_to_path = {item[0]: item[1] for item in all_sample_files}
        original_files = [label_to_path[lbl] for lbl in selected_labels]
    else:
        st.sidebar.error("No .wav sample files found in data/raw/speech or data/raw/music.")
        st.stop()

else:
    # Accept multiple .wav uploads; limit to 3 files
    uploaded_file_list = st.sidebar.file_uploader(
        "Upload WAV files (up to 3)",
        type=["wav"],
        accept_multiple_files=True,
        help="Select up to 3 .wav files at once"
    )
    if uploaded_file_list:
        for uf in uploaded_file_list[:3]:
            save_path = os.path.join(raw_dir, uf.name)
            with open(save_path, "wb") as f:
                f.write(uf.getbuffer())
            original_files.append(save_path)
    else:
        st.info("Please upload one or more .wav files from the sidebar to start.")
        st.stop()

# Stop early if no files were selected yet
if not original_files:
    st.info("Please select at least one audio file from the sidebar to start.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR — ENCODING SETTINGS
# ─────────────────────────────────────────────
st.sidebar.header("2. Encoding Settings")

# Single target bitrate applied to all files in this run
target_bitrate = st.sidebar.select_slider(
    "Select Target Bitrate (kbps):",
    options=["32k", "64k", "128k", "320k"],
    value="128k"
)

# ─────────────────────────────────────────────
# MAIN PANEL — ONE TAB PER FILE
# ─────────────────────────────────────────────
if st.sidebar.button("Run Analysis"):

    # Create one tab per selected file, labelled by filename
    file_tab_labels = [os.path.basename(f) for f in original_files]
    file_tabs = st.tabs(file_tab_labels)

    for i, original_file in enumerate(original_files):
        with file_tabs[i]:

            # ── Per-file mode selector ──────────────────────────────────────
            # Each file gets its own evaluation mode so that a speech file and
            # a music file can be analysed correctly in the same run.
            audio_mode = st.selectbox(
                "Evaluation Mode for this file:",
                ["Speech", "Music"],
                key=f"mode_{i}",        # unique key required by Streamlit
                help="Speech → STOI (intelligibility). Music → Spectral Cosine Similarity."
            ).lower()

            with st.spinner(f"Processing {os.path.basename(original_file)} in {audio_mode} mode..."):

                # ── Encoding ───────────────────────────────────────────────
                # Record wall-clock time to compute encoding latency
                start_time = time.time()

                # Compress the WAV file to MP3 at the chosen bitrate via FFmpeg
                results_dict = encode_audio(
                    input_filepath=original_file,
                    output_dir=output_dir,
                    bitrates=[target_bitrate],
                    fmt="mp3"
                )

                # Latency = total time taken to encode this file
                processing_latency = time.time() - start_time

                # Retrieve the path of the encoded output file
                comp_file = results_dict[target_bitrate]

                # ── Metrics ────────────────────────────────────────────────
                # Compute SNR, perceptual score, bitrate, and compression ratio
                # using the mode selected specifically for this file
                metrics = calculate_metrics(original_file, comp_file, mode=audio_mode)

                # ── Results layout ─────────────────────────────────────────
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Evaluation Metrics")
                    st.info(f"Active analysis mode: **{audio_mode.upper()}**")

                    # Row 1: SNR | perceptual score | bitrate
                    m1, m2, m3 = st.columns(3)
                    m1.metric("SNR (dB)", f"{metrics['snr']:.3f}")

                    # Label changes depending on the mode used for this file
                    score_label = "STOI Score" if audio_mode == "speech" else "Cosine Sim."
                    m2.metric(score_label, f"{metrics['perceptual_score']:.3f}")

                    m3.metric("Bitrate (kbps)", f"{metrics['bitrate'] / 1000:.1f}")

                    # Row 2: compression ratio | latency
                    m4, m5, _ = st.columns(3)
                    m4.metric("Compression Ratio", f"{metrics['compression_ratio']:.3f}")
                    m5.metric("Latency (s)", f"{processing_latency:.3f}")

                with col2:
                    st.subheader("🎧 Audio Comparison")
                    st.write("Original Source:")
                    st.audio(original_file)
                    st.write(f"Encoded Output ({target_bitrate}):")
                    st.audio(comp_file)

            # ── Visualizations ─────────────────────────────────────────────
            st.subheader("Visual Analysis")
            vtab1, vtab2 = st.tabs(["Spectrogram Comparison", "Waveform Comparison"])

            with vtab1:
                # Generate and display side-by-side spectrogram (STFT magnitude in dB)
                spec_path = plot_spectrogram_comparison(
                    original_file, comp_file,
                    os.path.join(img_dir, "spectrogram")
                )
                st.image(spec_path, use_container_width=True)

            with vtab2:
                # Generate and display side-by-side time-domain waveforms
                wave_path = plot_waveform_comparison(
                    original_file, comp_file,
                    os.path.join(img_dir, "waveform")
                )
                st.image(wave_path, use_container_width=True)

else:
    st.info("Configure parameters in the sidebar and click 'Run Analysis' to begin.")