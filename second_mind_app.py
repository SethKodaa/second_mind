import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Second Mind", layout="centered")
st.title("🧠 Second Mind")
st.caption("Your personal communication companion — transcribe audio and analyze tone")

# Load Whisper model (only once)
@st.cache_resource
def load_model():
    return whisper.load_model("base")  # You can use "small" for better accuracy

model = load_model()

# --- AUDIO UPLOAD ---
st.markdown("### 🎤 Transcribe Audio")
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "m4a", "wav", "ogg", "flac"])

if audio_file:
    st.audio(audio_file)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        temp_path = tmp_file.name

    with st.spinner("Transcribing..."):
        result = model.transcribe(temp_path)
        st.success("Done!")
        st.subheader("📝 Transcript")
        st.text_area("Transcript", result["text"], height=300)

    os.remove(temp_path)

# --- PASTE TEXT ---
st.