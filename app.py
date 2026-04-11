import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.encoder import encode_audio
from src.metrics import calculate_metrics
from src.visualization import plot_spectrogram_comparison, plot_waveform_comparison

st.set_page_config(page_title="Audio Codec Analyzer", layout="wide")

st.title("🎵 Audio Encoding & Quality Evaluation Dashboard")
st.markdown("Project: Audio Encoding Performance Evaluation")

st.sidebar.header("1. Input Audio")
input_option = st.sidebar.radio("Data Source:", ["Use Sample File", "Upload Custom File (.wav)"])

output_dir = "data/encode"
img_dir = "results"
raw_dir = "data/raw/uploads"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)
os.makedirs(raw_dir, exist_ok=True)

if input_option == "Use Sample File":
    input_type = st.sidebar.selectbox("Select Audio Type:", ["Speech", "Music"])
    folder_path = f"data/raw/{input_type.lower()}"
    
    if os.path.exists(folder_path):
        available_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
        if available_files:
            selected_filename = st.sidebar.selectbox(f"Select {input_type} file:", available_files)
            original_file = os.path.join(folder_path, selected_filename)
        else:
            st.sidebar.error(f"No .wav files found in '{folder_path}'.")
            st.stop()
    else:
        st.sidebar.error(f"Directory not found: {folder_path}")
        st.stop()
else:
    uploaded_file = st.sidebar.file_uploader("Upload WAV file", type=["wav"])
    if uploaded_file is not None:
        original_file = os.path.join(raw_dir, uploaded_file.name)
        with open(original_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        st.info("Please upload a .wav file from the sidebar to start.")
        st.stop()

st.sidebar.header("2. Encoding Settings")
target_bitrate = st.sidebar.select_slider(
    "Select Target Bitrate (kbps):",
    options=["32k", "64k", "128k", "320k"],
    value="128k"
)

if st.sidebar.button("Run Analysis"):
    with st.spinner("Processing audio..."):
        results_dict = encode_audio(
            input_filepath=original_file,
            output_dir=output_dir,
            bitrates=[target_bitrate],   
            fmt="mp3"
        )
        
        comp_file = results_dict[target_bitrate]
        metrics = calculate_metrics(original_file, comp_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Evaluation Metrics")
            m1, m2, m3 = st.columns(3)
            m1.metric("SNR (dB)", f"{metrics['snr']:.2f}")
            m2.metric("STOI", f"{metrics['stoi']:.4f}")
            m3.metric("Bitrate (bps)", f"{metrics['bitrate']:.0f}")
            
        with col2:
            st.subheader("🎧 Audio Comparison")
            st.write("Original (.wav):")
            st.audio(original_file)
            st.write(f"Compressed ({target_bitrate} MP3):")
            st.audio(comp_file)

        st.divider()

        st.subheader("📊 Visual Analysis")
        
        tab1, tab2 = st.tabs(["Spectrogram", "Waveform"])
        
        with tab1:
            spec_path = plot_spectrogram_comparison(original_file, comp_file, os.path.join(img_dir, "spectrogram"))
            st.image(spec_path, use_container_width=True)
            
        with tab2:
            wave_path = plot_waveform_comparison(original_file, comp_file, os.path.join(img_dir, "waveform"))
            st.image(wave_path, use_container_width=True)
else:
    st.info("Click 'Run Analysis' to start processing.")