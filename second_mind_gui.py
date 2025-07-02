import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Second Mind", layout="centered")
st.title("🧠 Second Mind")
st.subheader("Transcribe audio or paste text to analyze tone and intent")

# Load Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# --- AUDIO UPLOAD + TRANSCRIPTION ---
st.markdown("### 🎤 Upload Audio File")
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "m4a", "wav", "ogg", "webm", "flac", "aac", "mp4", "mkv", "avi"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_file_path = tmp_file.name

    with st.spinner("Transcribing with Whisper..."):
        result = model.transcribe(tmp_file_path)
        st.success("Transcription complete!")

    st.subheader("📝 Transcript from Audio")
    st.text_area("Transcript", result["text"], height=300)

    os.remove(tmp_file_path)

# --- MANUAL TEXT ENTRY ---
st.markdown("### ✍️ Paste a message for tone/intent analysis")
user_text = st.text_area("Paste your email, SMS, or chat message here", height=200)

if user_text.strip():
    st.markdown("#### ✅ Message received")
    st.write(user_text)

    # 🔮 Placeholder tone/intent analysis (basic keyword detection)
    st.markdown("#### 🧠 Analysis")
    if "sorry" in user_text.lower():
        st.info("This message might sound apologetic.")
    elif "urgent" in user_text.lower():
        st.warning("This might come off as intense or high-pressure.")
    elif "please" in user_text.lower() and "thank" in user_text.lower():
        st.success("This seems polite and respectful.")
    else:
        st.success("This seems neutral or conversational.")
