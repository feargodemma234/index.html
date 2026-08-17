import io
import re
import wave
import html
import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Quantum AI",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at top right,
                    rgba(86, 55, 190, 0.25),
                    transparent 35%
                ),
                radial-gradient(
                    circle at top left,
                    rgba(45, 35, 120, 0.20),
                    transparent 30%
                ),
                #070912;
            color: white;
        }

        section[data-testid="stSidebar"] {
            background: #0d1020;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] h1 {
            color: white;
        }

        .quantum-header {
            display: flex;
            align-items: center;
            gap: 18px;
            padding: 10px 0 25px 0;
        }

        .quantum-icon {
            width: 70px;
            height: 70px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            background: linear-gradient(
                135deg,
                #5b35ff,
                #8b5cf6
            );
            box-shadow:
                0 0 30px rgba(116, 82, 255, 0.35);
        }

        .quantum-title {
            font-size: 42px;
            font-weight: 800;
            line-height: 1;
        }

        .quantum-status {
            margin-top: 8px;
            color: #aeb4c7;
            font-size: 15px;
        }

        .online-dot {
            display: inline-block;
            width: 9px;
            height: 9px;
            background: #54e38e;
            border-radius: 50%;
            margin-right: 7px;
            box-shadow: 0 0 12px rgba(84,227,142,0.7);
        }

        .welcome-card {
            padding: 40px 25px;
            margin: 20px 0 30px 0;
            text-align: center;
            border-radius: 25px;
            background: rgba(22, 25, 37, 0.82);
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow: 0 20px 60px rgba(0,0,0,0.25);
        }

        .welcome-icon {
            font-size: 55px;
            margin-bottom: 12px;
        }

        .welcome-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .welcome-text {
            color: #aeb4c7;
            font-size: 16px;
            line-height: 1.6;
        }

        .voice-card {
            padding: 35px;
            border-radius: 25px;
            background: rgba(22, 25, 37, 0.82);
            border: 1px solid rgba(255,255,255,0.07);
            margin: 20px 0;
        }

        .voice-title {
            font-size: 30px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .voice-description {
            color: #aeb4c7;
            line-height: 1.6;
        }

        .section-title {
            font-size: 24px;
            font-weight: 700;
            margin-top: 25px;
            margin-bottom: 15px;
        }

        .chat-user {
            padding: 15px 18px;
            margin: 12px 0;
            border-radius: 18px;
            background: rgba(70, 58, 170, 0.25);
            border: 1px solid rgba(120,100,255,0.20);
        }

        .chat-ai {
            padding: 15px 18px;
            margin: 12px 0 22px 0;
            border-radius: 18px;
            background: rgba(25, 29, 42, 0.95);
            border: 1px solid rgba(255,255,255,0.06);
        }

        .chat-label {
            font-size: 12px;
            color: #9da4bb;
            margin-bottom: 6px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .error-box {
            padding: 18px;
            border-radius: 15px;
            background: rgba(180, 45, 55, 0.18);
            border: 1px solid rgba(255, 90, 100, 0.35);
            color: #ff9da4;
        }

        .info-box {
            padding: 18px;
            border-radius: 15px;
            background: rgba(45, 100, 180, 0.16);
            border: 1px solid rgba(90, 150, 255, 0.25);
            color: #b9d5ff;
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

if "voice_messages" not in st.session_state:
    st.session_state.voice_messages = []

if "last_voice_audio" not in st.session_state:
    st.session_state.last_voice_audio = None


# ============================================================
# API
# ============================================================

def get_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error(
            "GROQ_API_KEY was not found in Streamlit Secrets."
        )
        st.stop()

    return Groq(api_key=api_key)


client = get_client()


# ============================================================
# AI SETTINGS
# ============================================================

CHAT_MODEL = "llama-3.1-8b-instant"
STT_MODEL = "whisper-large-v3-turbo"
TTS_MODEL = "canopylabs/orpheus-v1-english"
TTS_VOICE = "autumn"


SYSTEM_PROMPT = """
You are Quantum AI, the central intelligence assistant
of the Quantum Administration Empire.

Be direct, helpful, intelligent and natural.

The Quantum Administration Empire has divisions including:
AI, Robotics, Energy, Health, Space, Sports,
Manufacturing, Infrastructure, Defense and Exploration.

Do not reveal hidden reasoning or internal chain-of-thought.
Give the user the useful answer directly.

For voice conversations, keep responses natural and
reasonably concise.
"""


# ============================================================
# AI CHAT
# ============================================================

def ask_quantum(messages):
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ] + messages,
        temperature=0.7,
        max_tokens=2048,
    )

    return response.choices[0].message.content.strip()


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_for_voice(text):
    """
    Remove markdown/code formatting that sounds bad when spoken.
    """
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    text = text.replace("•", "")
    text = text.replace("—", ", ")
    text = text.replace("–", ", ")

    return " ".join(text.split()).strip()


# ============================================================
# SPLIT TEXT FOR ORPHEUS
# ============================================================

def split_for_tts(text, max_chars=190):
    """
    Groq's current Orpheus documentation specifies a
    maximum input length of 200 characters.

    We stay below the limit to leave room for safety.
    """

    text = clean_for_voice(text)

    if not text:
        return []

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

        if len(sentence) <= max_chars:
            candidate = (
                sentence
                if not current
                else current + " " + sentence
            )

            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)

                current = sentence

        else:
            words = sentence.split()

            for word in words:
                candidate = (
                    word
                    if not current
                    else current + " " + word
                )

                if len(candidate) <= max_chars:
                    current = candidate
                else:
                    if current:
                        chunks.append(current)

                    current = word

    if current:
        chunks.append(current)

    return chunks


# ============================================================
# GROQ TTS
# ============================================================

def generate_tts(text):
    """
    Generate multiple WAV chunks and combine them into
    one continuous WAV file.
    """

    chunks = split_for_tts(text)

    if not chunks:
        return None

    audio_parts = []

    for chunk in chunks:

        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=chunk,
            response_format="wav",
        )

        audio_bytes = response.read()

        audio_parts.append(audio_bytes)

    return combine_wav_files(audio_parts)


# ============================================================
# COMBINE WAV FILES
# ============================================================

def combine_wav_files(wav_files):

    if not wav_files:
        return None

    output = io.BytesIO()

    first = wave.open(
        io.BytesIO(wav_files[0]),
        "rb"
    )

    params = first.getparams()
    frames = [first.readframes(first.getnframes())]
    first.close()

    for data in wav_files[1:]:

        wav = wave.open(
            io.BytesIO(data),
            "rb"
        )

        frames.append(
            wav.readframes(wav.getnframes())
        )

        wav.close()

    with wave.open(output, "wb") as final:

        final.setnchannels(params.nchannels)
        final.setsampwidth(params.sampwidth)
        final.setframerate(params.framerate)

        for frame in frames:
            final.writeframes(frame)

    return output.getvalue()


# ============================================================
# SPEECH TO TEXT
# ============================================================

def transcribe_audio(audio_file):

    audio_bytes = audio_file.getvalue()

    if not audio_bytes:
        return ""

    result = client.audio.transcriptions.create(
        file=(
            "recording.wav",
            audio_bytes,
            "audio/wav",
        ),
        model=STT_MODEL,
        language="en",
        response_format="text",
    )

    if isinstance(result, str):
        return result.strip()

    return getattr(
        result,
        "text",
        ""
    ).strip()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:26px;
            font-weight:800;
            margin-bottom:5px;
        ">
            ⚛️ Quantum OS
        </div>

        <div style="
            color:#9da4bb;
            margin-bottom:25px;
        ">
            Central Intelligence
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        [
            "🧠 Quantum AI",
            "🎙️ Quantum Voice",
            "🏢 Divisions",
            "⚙️ Settings",
        ],
    )

    st.divider()

    st.caption("System")
    st.write("🟢 Online")
    st.caption("Vision: Disabled")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="quantum-header">

        <div class="quantum-icon">
            ⚛️
        </div>

        <div>
            <div class="quantum-title">
                Quantum AI
            </div>

            <div class="quantum-status">
                <span class="online-dot"></span>
                Online • Central Intelligence
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# QUANTUM AI — TEXT
# ============================================================

if page == "🧠 Quantum AI":

    st.markdown(
        """
        <div class="welcome-card">

            <div class="welcome-icon">
                ⚛️
            </div>

            <div class="welcome-title">
                How can I help?
            </div>

            <div class="welcome-text">
                Talk with Quantum AI through text.
                Voice is available separately in the sidebar.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # Existing conversation
    for message in st.session_state.messages:

        if message["role"] == "user":

            safe_text = html.escape(message["content"])

            st.markdown(
                f"""
                <div class="chat-user">
                    <div class="chat-label">
                        You
                    </div>
                    {safe_text}
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            safe_text = html.escape(message["content"])
            safe_text = safe_text.replace("\n", "<br>")

            st.markdown(
                f"""
                <div class="chat-ai">
                    <div class="chat-label">
                        Quantum AI
                    </div>
                    {safe_text}
                </div>
                """,
                unsafe_allow_html=True,
            )

    user_text = st.chat_input(
        "Message Quantum AI..."
    )

    if user_text:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_text,
            }
        )

        with st.spinner("Quantum AI is thinking..."):

            try:

                answer = ask_quantum(
                    st.session_state.messages
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                st.rerun()

            except Exception as e:

                st.markdown(
                    f"""
                    <div class="error-box">
                        <b>Quantum AI error</b><br><br>
                        {html.escape(str(e))}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================
# QUANTUM VOICE
# ============================================================

elif page == "🎙️ Quantum Voice":

    st.markdown(
        """
        <div class="voice-card">

            <div class="voice-title">
                🎙️ Quantum Voice
            </div>

            <div class="voice-description">
                Speak to Quantum AI. Your recording is
                transcribed, sent to the AI, and the response
                is converted back into speech.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Tap the microphone, speak, then stop the recording."
    )

    audio_input = st.audio_input(
        "🎙️ Record your message"
    )

    if audio_input:

        with st.spinner(
            "Listening and transcribing..."
        ):

            try:

                transcript = transcribe_audio(
                    audio_input
                )

            except Exception as e:

                transcript = ""

                st.markdown(
                    f"""
                    <div class="error-box">
                        <b>Speech recognition error</b><br><br>
                        {html.escape(str(e))}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if transcript:

            st.markdown(
                f"""
                <div class="chat-user">

                    <div class="chat-label">
                        You said
                    </div>

                    {html.escape(transcript)}

                </div>
                """,
                unsafe_allow_html=True,
            )

            voice_history = (
                st.session_state.voice_messages
                + [
                    {
                        "role": "user",
                        "content": transcript,
                    }
                ]
            )

            with st.spinner(
                "Quantum AI is responding..."
            ):

                try:

                    answer = ask_quantum(
                        voice_history
                    )

                    st.session_state.voice_messages.append(
                        {
                            "role": "user",
                            "content": transcript,
                        }
                    )

                    st.session_state.voice_messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                except Exception as e:

                    answer = ""

                    st.markdown(
                        f"""
                        <div class="error-box">
                            <b>AI response error</b><br><br>
                            {html.escape(str(e))}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            if answer:

                st.markdown(
                    f"""
                    <div class="chat-ai">

                        <div class="chat-label">
                            Quantum AI
                        </div>

                        {html.escape(answer).replace(
                            chr(10), "<br>"
                        )}

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.spinner(
                    "Preparing Quantum AI's voice..."
                ):

                    try:

                        audio = generate_tts(
                            answer
                        )

                        if audio:

                            st.session_state.last_voice_audio = audio

                            st.audio(
                                audio,
                                format="audio/wav",
                                autoplay=True,
                            )

                        else:

                            st.warning(
                                "No voice audio was generated."
                            )

                    except Exception as e:

                        error_text = str(e)

                        if (                            "terms" in error_text.lower()
                            or "model_terms_required"
                            in error_text.lower()
                        ):

                            st.markdown(
                                """
                                <div class="error-box">

                                <b>
                                Quantum Voice needs
                                Groq model terms acceptance.
                                </b>

                                <br><br>

                                The Orpheus voice model requires
                                your Groq organization administrator
                                to accept its terms before the
                                model can generate audio.

                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        else:

                            st.markdown(
                                f"""
                                <div class="error-box">

                                <b>
                                Voice generation error
                                </b>

                                <br><br>

                                {html.escape(error_text)}

                                </div>
                                """,
                                unsafe_allow_html=True,
                            )


# ============================================================
# PREVIOUS VOICE CONVERSATION
# ============================================================

    if st.session_state.voice_messages:

        st.markdown(
            '<div class="section-title">Conversation</div>',
            unsafe_allow_html=True,
        )

        for message in st.session_state.voice_messages:

            label = (
                "You"
                if message["role"] == "user"
                else "Quantum AI"
            )

            css_class = (
                "chat-user"
                if message["role"] == "user"
                else "chat-ai"
            )

            safe_content = html.escape(
                message["content"]
            ).replace("\n", "<br>")

            st.markdown(
                f"""
                <div class="{css_class}">

                    <div class="chat-label">
                        {label}
                    </div>

                    {safe_content}

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# DIVISIONS
# ============================================================

elif page == "🏢 Divisions":

    st.markdown(
        """
        <div class="welcome-card">

            <div class="welcome-icon">
                🏢
            </div>

            <div class="welcome-title">
                Quantum Administration Empire
            </div>

            <div class="welcome-text">
                A connected network of technology,
                science, engineering and infrastructure
                divisions.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    divisions = [
        ("🤖", "AI"),
        ("🦾", "Robotics"),
        ("⚡", "Energy"),
        ("🧬", "Health"),
        ("🚀", "Space"),
        ("🏆", "Sports"),
        ("🏭", "Manufacturing"),
        ("🏗️", "Infrastructure"),
        ("🛡️", "Defense"),
        ("🌍", "Exploration"),
    ]

    cols = st.columns(2)

    for index, (icon, name) in enumerate(divisions):

        with cols[index % 2]:

            st.markdown(
                f"""
                <div class="chat-ai">

                    <div style="
                        font-size:25px;
                        margin-bottom:5px;
                    ">
                        {icon}
                    </div>

                    <div style="
                        font-size:20px;
                        font-weight:700;
                    ">
                        {name}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    st.markdown(
        """
        <div class="section-title">
            ⚙️ Quantum AI Settings
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Configure the assistant from this section."
    )

    st.write(
        f"🧠 Text model: `{CHAT_MODEL}`"
    )

    st.write(
        f"🎙️ Speech recognition: `{STT_MODEL}`"
    )

    st.write(
        f"🔊 Voice model: `{TTS_MODEL}`"
    )

    st.write(
        f"🎧 Voice: `{TTS_VOICE}`"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Text Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.rerun()

    if st.button(
        "🗑️ Clear Voice Conversation",
        use_container_width=True,
    ):

        st.session_state.voice_messages = []
        st.rerun()

    st.divider()

    st.markdown(
        """
        <div class="info-box">

        <b>Vision is disabled.</b>

        Quantum AI currently uses text and voice only.

        </div>
        """,
        unsafe_allow_html=True,
    )
                  