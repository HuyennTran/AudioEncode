import streamlit as st
import os
from src.encoder import encode_audio
from src.metrics import calculate_metrics
from src.visualize import plot_spectrogram_comparison, plot_waveform_comparison

# Cấu hình trang
st.set_page_config(page_title="Audio Codec Analyzer", layout="wide")

st.title("🎵 Audio Encoding & Quality Evaluation Dashboard")
st.markdown("Dự án: Đánh giá hiệu năng mã hóa âm thanh (MP3) - Nhóm Huyền & Diệp")

# Sidebar - Điều khiển
st.sidebar.header("Control Panel")

# 1. Chọn dữ liệu đầu vào
input_type = st.sidebar.selectbox("Chọn loại âm thanh:", ["Speech", "Music"])
if input_type == "Speech":
    original_file = "data/raw/speech/speech_female.wav"
else:
    original_file = "data/raw/music/music_orchestra.wav"

# 2. Chọn Bitrate mục tiêu
bitrate = st.sidebar.select_slider(
    "Chọn Target Bitrate (kbps):",
    options=["32k", "64k", "128k", "320k"],
    value="128k"
)

# Thư mục lưu kết quả tạm
output_dir = "data/encode"
img_dir = "results"

if st.sidebar.button("Run Analysis"):
    with st.spinner("Đang xử lý..."):
        # Bước 1: Mã hóa
        comp_file = encode_audio(original_file, bitrate, output_dir)
        
        # Bước 2: Tính toán Metrics
        metrics = calculate_metrics(original_file, comp_file)
        
        # Bước 3: Render giao diện kết quả
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Kế quả đo lường (Metrics)")
            st.metric("Compression Ratio (CR)", f"{metrics['compression_ratio']:.2f}x")
            st.metric("SNR (dB)", f"{metrics['snr']:.2d} dB")
            
        with col2:
            st.subheader("🎧 Nghe thử")
            st.write("Bản gốc (.wav):")
            st.audio(original_file)
            st.write(f"Bản nén ({bitrate} MP3):")
            st.audio(comp_file)

        st.divider()

        # Bước 4: Hiển thị hình ảnh trực quan
        st.subheader("📊 Phân tích trực quan (Visual Analysis)")
        
        tab1, tab2 = st.tabs(["Spectrogram (Phổ tần số)", "Waveform (Dạng sóng)"])
        
        with tab1:
            spec_path = plot_spectrogram_comparison(original_file, comp_file, os.path.join(img_dir, "spectrogram"))
            st.image(spec_path, caption=f"So sánh Spectrogram: Gốc vs {bitrate}")
            st.info("💡 Mẹo: Quan sát dải tần số cao (phần trên cùng) để thấy sự cắt gọt của thuật toán nén.")
            
        with tab2:
            wave_path = plot_waveform_comparison(original_file, comp_file, os.path.join(img_dir, "waveform"))
            st.image(wave_path, caption=f"So sánh Waveform: Gốc vs {bitrate}")

else:
    st.info("Vui lòng chọn thông số ở thanh bên trái và nhấn 'Run Analysis' để bắt đầu.")