import io
import wave
import re

import streamlit as st
from groq import Groq


# ============================================================
# QUANTUM AI
# Text + Voice
# Vision intentionally NOT included
# ============================================================


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="Quantum AI",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# GROQ CLIENT
# ------------------------------------------------------------

@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


client = get_client()


# ------------------------------------------------------------
# MODELS
# ------------------------------------------------------------

CHAT_MODEL = "llama3-70b-8192"
STT_MODEL = "whisper-large-v3-turbo"
TTS_MODEL = "canopylabs/orpheus-v1-english"

# Change this if you want another supported Orpheus voice.
TTS_VOICE = "troy"


# ------------------------------------------------------------
# SYSTEM PROMPT
# ------------------------------------------------------------

SYSTEM_PROMPT = """
You are Quantum AI, the central intelligence of Quantum OS.

Be direct, helpful, intelligent, and conversational.

Do not reveal hidden reasoning or internal chain-of-thought.
Do not write <think> sections.
Do not describe your internal reasoning process.

Answer the user's question directly.

The Quantum Administration Empire is a project with divisions including:
AI, Robotics, Energy, Health, Space, Sports,
Manufacturing, Infrastructure, Defense, and Exploration.

When discussing the project, help organize ideas clearly and practically.
"""


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_messages" not in st.session_state:
    st.session_state.voice_messages = []

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None


# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(90, 70, 200, 0.25),
                transparent 35%
            ),
            #070914;
    }

    [data-testid="stSidebar"] {
        background: #0b0e1b;
    }

    .quantum-header {
        padding: 25px 0 10px 0;
    }

    .quantum-title {
        font-size: 46px;
        font-weight: 800;
        margin: 0;
    }

    .quantum-subtitle {
        color: #a8adbd;
        font-size: 17px;
        margin-top: 5px;
    }

    .status {
        color: #8f96a8;
        margin-top: 5px;
    }

    .welcome-box {
        padding: 35px;
        border-radius: 24px;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 25px;
    }

    .welcome-title {
        font-size: 30px;
        font-weight: 700;
    }

    .welcome-text {
        color: #aeb4c4;
        font-size: 17px;
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    st.markdown("# ⚛️ Quantum OS")
    st.caption("Quantum Administration Empire")

    st.divider()

    page = st.radio(
        "System",
        [
            "🏠 Home",
            "💬 Quantum AI",
            "🎙️ Quantum Voice",
            "🏢 Divisions",
            "⚙️ Settings",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("Quantum OS")
    st.caption("Central Intelligence System")


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def clean_response(text):
    """
    Removes accidental reasoning tags if a model returns them.
    """

    if not text:
        return ""

    # Remove <think>...</think>
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Remove stray tags
    text = text.replace("<think>", "")
    text = text.replace("</think>", "")

    return text.strip()


def ask_quantum(messages):
    """
    Send conversation to Groq.
    """

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=4096,
    )

    answer = response.choices[0].message.content

    return clean_response(answer)


def split_for_voice(text, max_chars=180):
    """
    Orpheus has a 200-character input limit.
    We stay below that limit to leave some safety room.
    """

    text = text.strip()

    if not text:
        return []

    # First split at sentence boundaries.
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    chunks = []
    current = ""

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        # If sentence itself is too long, split by words.
        if len(sentence) > max_chars:

            words = sentence.split()

            for word in words:

                candidate = (
                    current + " " + word
                    if current
                    else word
                )

                if len(candidate) <= max_chars:
                    current = candidate

                else:

                    if current:
                        chunks.append(current)

                    current = word

        else:

            candidate = (
                current + " " + sentence
                if current
                else sentence
            )

            if len(candidate) <= max_chars:
                current = candidate

            else:

                if current:
                    chunks.append(current)

                current = sentence

    if current:
        chunks.append(current)

    return chunks


def generate_speech(text):
    """
    Generate complete speech from a long AI response.

    Every chunk is sent separately because Orpheus
    accepts a maximum of 200 characters per request.
    """

    chunks = split_for_voice(text)

    if not chunks:
        return None

    audio_files = []

    for chunk in chunks:

        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=chunk,
            response_format="wav",
        )

        audio_files.append(response.read())

    return combine_wav(audio_files)


def combine_wav(files):
    """
    Combine multiple WAV files into one complete WAV file.
    """

    if not files:
        return None

    output = io.BytesIO()

    first = wave.open(
        io.BytesIO(files[0]),
        "rb"
    )

    params = first.getparams()

    with wave.open(output, "wb") as combined:

        combined.setparams(params)

        for data in files:

            wav = wave.open(
                io.BytesIO(data),
                "rb"
            )

            combined.writeframes(
                wav.readframes(
                    wav.getnframes()
                )
            )

            wav.close()

    first.close()

    return output.getvalue()


def transcribe_audio(audio_bytes):
    """
    Convert microphone recording into text.
    """

    result = client.audio.transcriptions.create(
        file=("voice.wav", audio_bytes),
        model=STT_MODEL,
        language="en",
        temperature=0,
    )

    return result.text.strip()


def add_message(role, content):

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown(
        """
        <div class="quantum-header">

        <div class="quantum-title">
        ⚛️ Quantum AI
        </div>

        <div class="quantum-subtitle">
        Central Intelligence System
        </div>

        <div class="status">
        ● Online
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="welcome-box">

        <div class="welcome-title">
        Welcome to Quantum OS
        </div>

        <div class="welcome-text">

        Quantum AI is the central intelligence interface
        for the Quantum Administration Empire.

        Use the sidebar to choose how you want to interact:

        <br><br>

        💬 <b>Quantum AI</b> — type messages.

        <br>

        🎙️ <b>Quantum Voice</b> — speak to Quantum AI
        and receive a spoken response.

        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TEXT AI
# ============================================================

elif page == "💬 Quantum AI":

    st.markdown(
        """
        <div class="quantum-header">

        <div class="quantum-title">
        ⚛️ Quantum AI
        </div>

        <div class="quantum-subtitle">
        Text Intelligence
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # Show chat history
    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    user_input = st.chat_input(
        "Message Quantum AI..."
    )

    if user_input:

        add_message(
            "user",
            user_input
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        api_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        api_messages.extend(
            st.session_state.messages
        )

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = ask_quantum(
                        api_messages
                    )

                    st.markdown(answer)

                    add_message(
                        "assistant",
                        answer
                    )

                except Exception as e:

                    st.error(
                        f"Quantum AI error: {e}"
                    )


# ============================================================
# VOICE AI
# ============================================================

elif page == "🎙️ Quantum Voice":

    st.markdown(
        """
        <div class="quantum-header">

        <div class="quantum-title">
        🎙️ Quantum Voice
        </div>

        <div class="quantum-subtitle">
        Speak directly with Quantum AI
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Press the microphone button, speak, and stop recording. "
        "Quantum AI will transcribe your voice, answer, and speak back."
    )

    audio_input = st.audio_input(
        "Speak to Quantum AI"
    )

    if audio_input is not None:

        audio_bytes = audio_input.getvalue()

        try:

            # ----------------------------------------------
            # STEP 1 — SPEECH TO TEXT
            # ----------------------------------------------

            with st.spinner(
                "Listening..."
            ):

                user_text = transcribe_audio(
                    audio_bytes
                )

            if not user_text:

                st.warning(
                    "I couldn't detect any speech."
                )

            else:

                st.markdown("### You")

                st.write(user_text)

                # ------------------------------------------
                # STEP 2 — AI RESPONSE
                # ------------------------------------------

                voice_messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    }
                ]

                voice_messages.extend(
                    st.session_state.voice_messages
                )

                voice_messages.append(
                    {
                        "role": "user",
                        "content": user_text,
                    }
                )

                with st.spinner(
                    "Quantum AI is thinking..."
                ):

                    answer = ask_quantum(
                        voice_messages
                    )

                st.markdown("### Quantum AI")

                st.write(answer)

                # Save conversation
                st.session_state.voice_messages.append(
                    {
                        "role": "user",
                        "content": user_text,
                    }
                )

                st.session_state.voice_messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                # ------------------------------------------
                # STEP 3 — TEXT TO SPEECH
                # ------------------------------------------

                with st.spinner(
                    "Preparing voice..."
                ):

                    audio = generate_speech(
                        answer
                    )

                if audio:

                    st.session_state.last_audio = audio

                    st.audio(
                        audio,
                        format="audio/wav",
                        autoplay=True,
                    )

                    st.success(
                        "Quantum AI finished speaking."
                    )

        except Exception as e:

            st.error(
                f"Voice error: {e}"
            )

    # Replay button
    if st.session_state.last_audio:

        if st.button(
            "🔊 Replay last response"
        ):

            st.audio(
                st.session_state.last_audio,
                format="audio/wav",
                autoplay=True,
            )


# ============================================================
# DIVISIONS
# ============================================================

elif page == "🏢 Divisions":

    st.title("🏢 Quantum Administration Empire")

    st.write(
        "The major divisions of the empire."
    )

    divisions = [
        ("🤖", "AI"),
        ("🦾", "Robotics"),
        ("⚡", "Energy"),
        ("🏥", "Health"),
        ("🚀", "Space"),
        ("🏆", "Sports"),
        ("🏭", "Manufacturing"),
        ("🏗️", "Infrastructure"),
        ("🛡️", "Defense"),
        ("🌍", "Exploration"),
    ]

    for icon, name in divisions:

        st.markdown(
            f"### {icon} {name}"
        )


# ============================================================
# SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.write(
        "Quantum AI configuration."
    )

    st.write(
        f"**Chat model:** `{CHAT_MODEL}`"
    )

    st.write(
        f"**Speech recognition:** `{STT_MODEL}`"
    )

    st.write(
        f"**Voice model:** `{TTS_MODEL}`"
    )

    st.write(
        f"**Voice:** `{TTS_VOICE}`"
    )

    st.divider()

    if st.button(
        "🗑️ Clear text conversation"
    ):

        st.session_state.messages = []

        st.success(
            "Text conversation cleared."
        )

    if st.button(
        "🗑️ Clear voice conversation"
    ):

        st.session_state.voice_messages = []

        st.success(
            "Voice conversation cleared."
        )