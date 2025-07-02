import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Second Mind", layout="centered")
st.title("🧠 Second Mind")
st.caption("Your personal communication companion — transcribe audio and analyze tone")

# Load Whisper model (cached)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# --- AUDIO TRANSCRIPTION ---
st.markdown("### 🎤 Transcribe Audio")
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "m4a", "wav", "ogg", "flac"])

if audio_file:
    st.audio(audio_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        temp_path = tmp_file.name

    with st.spinner("Transcribing..."):
        result = model.transcribe(temp_path)
        st.success("Transcription complete!")

    st.subheader("📝 Transcript")
    st.text_area("Transcript", result["text"], height=300)

    os.remove(temp_path)

# --- MANUAL TEXT INPUT + BUTTON ---
st.markdown("### ✍️ Paste a Message")
user_text = st.text_area("Paste a message (email, SMS, or chat) to analyze tone", height=200)

if st.button("🧠 Analyse Text"):
    if user_text.strip():
        st.subheader("Tone Analysis")

        tone = "neutral"
        if "sorry" in user_text.lower():
            tone = "apologetic"
        elif "urgent" in user_text.lower():
            tone = "assertive or high-pressure"
        elif "please" in user_text.lower() and "thank" in user_text.lower():
            tone = "polite"

        st.info(f"Detected tone: **{tone}**")

        if tone == "apologetic":
            st.write("You may be expressing regret or softening the message.")
        elif tone == "assertive or high-pressure":
            st.write("Consider softening your language if the tone feels intense.")
        elif tone == "polite":
            st.write("Comes across as respectful and courteous.")
        else:
            st.write("Tone appears neutral or balanced.")
    else:
        st.warning("Please enter some text before clicking Analyse.")
