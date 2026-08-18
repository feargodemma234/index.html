import io
import re
import wave

import requests
import streamlit as st
from groq import Groq


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Quantum AI",
    page_icon="⚛️",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at top right, #21165c 0%, transparent 35%),
            radial-gradient(circle at top left, #101d45 0%, transparent 30%),
            #070914;
        color: white;
    }

    [data-testid="stSidebar"] {
        background: #0c0f1d;
        border-right: 1px solid #252943;
    }

    .quantum-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
    }

    .quantum-logo {
        width: 62px;
        height: 62px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 34px;
        background: linear-gradient(135deg, #7047ff, #9a5cff);
        box-shadow: 0 10px 35px rgba(112, 71, 255, 0.35);
    }

    .quantum-title {
        font-size: 34px;
        font-weight: 800;
        line-height: 1;
    }

    .quantum-status {
        color: #aeb5c9;
        margin-top: 8px;
        font-size: 14px;
    }

    .online-dot {
        color: #57e389;
    }

    .welcome {
        padding: 30px;
        border-radius: 24px;
        background: rgba(20, 23, 38, 0.82);
        border: 1px solid #292d46;
        text-align: center;
        margin-top: 20px;
    }

    .welcome-icon {
        font-size: 48px;
    }

    .welcome-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 10px;
    }

    .welcome-text {
        color: #aeb5c9;
        margin-top: 10px;
    }

    .voice-box {
        padding: 28px;
        border-radius: 24px;
        background: rgba(20, 23, 38, 0.85);
        border: 1px solid #292d46;
        text-align: center;
        margin: 20px 0;
    }

    .voice-icon {
        font-size: 60px;
    }

    .small-note {
        color: #9299ad;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_history" not in st.session_state:
    st.session_state.voice_history = []

if "page" not in st.session_state:
    st.session_state.page = "Text Chat"


# ============================================================
# GROQ CLIENT
# ============================================================

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error(
        "GROQ_API_KEY is missing. Add it to Streamlit Secrets before using Quantum AI."
    )
    st.stop()

client = Groq(api_key=api_key)


# ============================================================
# SETTINGS
# ============================================================

CHAT_MODEL = "llama-3.3-70b-versatile"
WHISPER_MODEL = "whisper-large-v3-turbo"
TTS_MODEL = "canopylabs/orpheus-v1-english"
TTS_VOICE = "troy"

SYSTEM_PROMPT = """
You are Quantum AI, the central intelligence assistant of the Quantum Administration Empire.

Be direct, useful, intelligent, and conversational.

Do not expose hidden reasoning or internal chain-of-thought.
Do not say things like "here is my thinking process" or "<think>".

Answer the user's actual question directly.

The Quantum Administration Empire has divisions including:
AI, Robotics, Energy, Health, Space, Sports, Manufacturing,
Infrastructure, Defense, and Exploration.

Do not pretend that you have capabilities that are not actually connected.
"""


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="quantum-header">
        <div class="quantum-logo">⚛️</div>
        <div>
            <div class="quantum-title">Quantum AI</div>
            <div class="quantum-status">
                <span class="online-dot">●</span>
                Online • Central Intelligence
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚛️ Quantum AI")
    st.caption("Choose how you want to communicate.")

    page = st.radio(
        "Mode",
        [
            "Text Chat",
            "Quantum Voice",
        ],
        index=0 if st.session_state.page == "Text Chat" else 1,
    )

    st.session_state.page = page

    st.divider()

    st.markdown("### Settings")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.voice_history = []
        st.rerun()

    st.divider()

    st.caption("Quantum AI")
    st.caption("Text + Voice")
    st.caption("Vision disabled")


# ============================================================
# AI CHAT FUNCTION
# ============================================================

def ask_quantum_ai(user_text, history):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_text,
        }
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
    )

    return response.choices[0].message.content.strip()


# ============================================================
# SPLIT TEXT FOR ORPHEUS
# ============================================================

def split_for_tts(text, max_chars=190):
    """
    Orpheus currently accepts max 200 characters per TTS request.
    We use 190 to leave some safety margin.
    """

    text = re.sub(r"\s+", " ", text).strip()

    if len(text) <= max_chars:
        return [text]

    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current = ""

    for sentence in sentences:

        if len(sentence) <= max_chars:

            if not current:
                current = sentence

            elif len(current) + 1 + len(sentence) <= max_chars:
                current += " " + sentence

            else:
                chunks.append(current)
                current = sentence

        else:

            words = sentence.split()

            for word in words:

                if not current:
                    current = word

                elif len(current) + 1 + len(word) <= max_chars:
                    current += " " + word

                else:
                    chunks.append(current)
                    current = word

    if current:
        chunks.append(current)

    return chunks


# ============================================================
# TTS
# ============================================================

def generate_tts(text):

    chunks = split_for_tts(text)

    audio_parts = []

    for chunk in chunks:

        response = requests.post(
            "https://api.groq.com/openai/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": TTS_MODEL,
                "input": chunk,
                "voice": TTS_VOICE,
                "response_format": "wav",
            },
            timeout=120,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"TTS error {response.status_code}: {response.text}"
            )

        audio_parts.append(response.content)

    return combine_wav_files(audio_parts)


# ============================================================
# COMBINE WAV FILES
# ============================================================

def combine_wav_files(files):

    if not files:
        return None

    output = io.BytesIO()

    first = wave.open(io.BytesIO(files[0]), "rb")

    params = first.getparams()

    output_wave = wave.open(output, "wb")
    output_wave.setnchannels(first.getnchannels())
    output_wave.setsampwidth(first.getsampwidth())
    output_wave.setframerate(first.getframerate())

    for data in files:

        wav = wave.open(io.BytesIO(data), "rb")

        frames = wav.readframes(wav.getnframes())

        output_wave.writeframes(frames)

        wav.close()

    first.close()
    output_wave.close()

    output.seek(0)

    return output.read()


# ============================================================
# SPEECH TO TEXT
# ============================================================

def transcribe_audio(audio_file):

    audio_bytes = audio_file.getvalue()

    result = client.audio.transcriptions.create(
        file=(
            audio_file.name or "voice_input.wav",
            audio_bytes,
        ),
        model=WHISPER_MODEL,
        language="en",
        temperature=0.0,
    )

    return result.text.strip()


# ============================================================
# TEXT CHAT PAGE
# ============================================================

if page == "Text Chat":

    st.markdown(
        """
        <div class="welcome">
            <div class="welcome-icon">💬</div>
            <div class="welcome-title">Welcome to Quantum AI</div>
            <div class="welcome-text">
                Ask anything and Quantum AI will respond directly.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Message Quantum AI...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Quantum AI is responding..."):

                try:

                    answer = ask_quantum_ai(
                        prompt,
                        st.session_state.messages[:-1],
                    )

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                except Exception as e:

                    st.error(f"Quantum AI error: {e}")


# ============================================================
# QUANTUM VOICE PAGE
# ============================================================

elif page == "Quantum Voice":

    st.markdown(
        """
        <div class="voice-box">
            <div class="voice-icon">🎙️</div>
            <h2>Quantum Voice</h2>
            <p>
                Speak to Quantum AI and receive a spoken response.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Press the microphone button, speak, then stop recording. "
        "Quantum AI will transcribe your speech, answer, and speak the response."
    )

    audio_input = st.audio_input(
        "🎙️ Tap to speak",
        key="quantum_voice_input",
    )

    if audio_input:

        with st.spinner("Listening..."):

            try:

                user_text = transcribe_audio(audio_input)

                if not user_text:
                    st.warning("I couldn't detect any speech.")
                    st.stop()

                st.markdown("### You")
                st.write(user_text)

                # Save user message
                st.session_state.voice_history.append(
                    {
                        "role": "user",
                        "content": user_text,
                    }
                )

                with st.spinner("Quantum AI is thinking..."):

                    answer = ask_quantum_ai(
                        user_text,
                        st.session_state.voice_history[:-1],
                    )

                st.markdown("### Quantum AI")
                st.write(answer)

                st.session_state.voice_history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                with st.spinner("Preparing voice..."):

                    audio = generate_tts(answer)

                st.audio(
                    audio,
                    format="audio/wav",
                    autoplay=True,
                )

            except Exception as e:

                error = str(e)

                if "model_terms_required" in error:

                    st.error(
                        "The Groq Orpheus voice model requires its terms "
                        "to be accepted in your Groq organization first."
                    )

                    st.info(
                        "After accepting the Orpheus model terms, restart "
                        "the Streamlit app and try Quantum Voice again."
                    )

                else:

                    st.error(
                        f"Voice error: {error}"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Quantum AI • Text and Voice are separate modes • Vision is disabled"
)