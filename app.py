import os
import json
import hashlib
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq


# ============================================================
# QUANTUM OS
# Text + Voice
# NO VISION
# ============================================================

st.set_page_config(
    page_title="Quantum OS",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIG
# ============================================================

CHAT_MODEL = "llama-3.3-70b-versatile"
VOICE_MODEL = "whisper-large-v3-turbo"

SYSTEM_PROMPT = """
You are Quantum AI, the central intelligence of the Quantum Administration Empire.

Be direct, intelligent, useful, and natural.

The Quantum Administration Empire contains these divisions:
- AI
- Robotics
- Energy
- Health
- Space
- Sports
- Manufacturing
- Infrastructure
- Defense
- Exploration

Answer the user's actual question directly.

Do not reveal hidden reasoning or internal chain-of-thought.
Do not begin answers with things like:
"<think>"
"Here's my thinking process"
"Analyze User Input"
"Identify Role/Context"

Do not describe your internal reasoning.

Use clear formatting when useful.
"""


# ============================================================
# API KEY
# ============================================================

def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass

    return os.environ.get("GROQ_API_KEY")


api_key = get_api_key()


# ============================================================
# GROQ CLIENT
# ============================================================

if api_key:
    client = Groq(api_key=api_key)
else:
    client = None


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_messages" not in st.session_state:
    st.session_state.voice_messages = []

if "last_voice_text" not in st.session_state:
    st.session_state.last_voice_text = ""

if "last_spoken_response" not in st.session_state:
    st.session_state.last_spoken_response = ""


# ============================================================
# CSS
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
        visibility: hidden;
    }

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(77, 52, 180, 0.25),
                transparent 35%
            ),
            #070914;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0c1020 0%,
                #080b16 100%
            );
    }

    .quantum-header {
        padding: 15px 0 10px 0;
    }

    .quantum-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .quantum-status {
        color: #a9adbd;
        font-size: 16px;
        margin-top: -5px;
    }

    .online-dot {
        color: #7dff9b;
    }

    .welcome {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 35px;
        margin-top: 25px;
        text-align: center;
    }

    .welcome-icon {
        font-size: 55px;
    }

    .welcome-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 10px;
    }

    .welcome-text {
        color: #aeb2c2;
        font-size: 16px;
        margin-top: 8px;
    }

    .voice-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 25px;
        margin-top: 20px;
    }

    .small-status {
        color: #aeb2c2;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="font-size:28px;font-weight:800;margin-bottom:25px;">
            ⚛️ Quantum OS
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### System")

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🤖 Quantum AI",
            "🎙️ Quantum Voice",
            "🏢 Divisions",
            "📁 Files",
            "⚙️ Settings",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        """
        <div style="color:#8f93a4;font-size:15px;">
        The Quantum Administration Empire
        </div>

        <div style="color:#686c7c;font-size:14px;margin-top:20px;">
        Quantum OS v1.0
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SAFETY / API STATUS
# ============================================================

if not api_key:

    st.error(
        "GROQ_API_KEY is missing. Add it to Streamlit Cloud → Manage app → Settings → Secrets."
    )

    st.stop()


# ============================================================
# AI FUNCTION
# ============================================================

def ask_quantum_ai(user_text, history=None):

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for message in history:

        role = message.get("role")

        if role in ["user", "assistant"]:

            content = message.get("content", "")

            if content:
                messages.append(
                    {
                        "role": role,
                        "content": content,
                    }
                )

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

    return response.choices[0].message.content


# ============================================================
# TEXT TO SPEECH
# Browser-based
# ============================================================

def speak_text(text, autoplay=True):

    if not text:
        return

    safe_text = json.dumps(text)

    autoplay_code = "speakNow();" if autoplay else ""

    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;background:transparent;">

        <script>

        const text = {safe_text};

        function speakNow() {{

            if (!("speechSynthesis" in window)) {{
                alert("Speech synthesis is not supported by this browser.");
                return;
            }}

            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);

            utterance.lang = "en-US";
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;

            window.speechSynthesis.speak(utterance);
        }}

        {autoplay_code}

        </script>

        <button
            onclick="speakNow()"
            style="
                width:100%;
                padding:12px;
                border:none;
                border-radius:12px;
                background:#25283a;
                color:white;
                font-size:15px;
                cursor:pointer;
            "
        >
            🔊 Play Voice
        </button>

        </body>
        </html>
        """,
        height=55,
        scrolling=False,
    )


# ============================================================
# SPEECH TO TEXT
# ============================================================

def transcribe_audio(audio_file):

    if audio_file is None:
        return ""

    audio_bytes = audio_file.getvalue()

    if not audio_bytes:
        return ""

    result = client.audio.transcriptions.create(
        file=(
            "recording.wav",
            audio_bytes,
            "audio/wav",
        ),
        model=VOICE_MODEL,
        language="en",
        temperature=0.0,
    )

    return result.text.strip()


# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown(
        """
        <div class="quantum-header">

            <div class="quantum-title">
                ⚛️ Quantum OS
            </div>

            <div class="quantum-status">
                <span class="online-dot">●</span>
                Online • Central Intelligence
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="welcome">

            <div class="welcome-icon">⚛️</div>

            <div class="welcome-title">
                Welcome to Quantum OS
            </div>

            <div class="welcome-text">
                Your central interface for the Quantum Administration Empire.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Use the sidebar to open Quantum AI for text chat or Quantum Voice for voice conversations."
    )


# ============================================================
# QUANTUM AI — TEXT ONLY
# ============================================================

elif page == "🤖 Quantum AI":

    st.markdown(
        """
        <div class="quantum-header">

            <div class="quantum-title">
                🤖 Quantum AI
            </div>

            <div class="quantum-status">
                <span class="online-dot">●</span>
                Online • Text Intelligence
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display conversation

    if not st.session_state.messages:

        st.markdown(
            """
            <div class="welcome">

                <div class="welcome-icon">🤖</div>

                <div class="welcome-title">
                    How can I help?
                </div>

                <div class="welcome-text">
                    Type a message below to talk with Quantum AI.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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

        with st.chat_message("user"):
            st.markdown(user_text)

        with st.chat_message("assistant"):

            with st.spinner("Quantum AI is thinking..."):

                try:

                    answer = ask_quantum_ai(
                        user_text,
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

                    st.error(
                        f"Quantum AI error: {str(e)}"
                    )


# ============================================================
# QUANTUM VOICE
# ============================================================

elif page == "🎙️ Quantum Voice":

    st.markdown(
        """
        <div class="quantum-header">

            <div class="quantum-title">
                🎙️ Quantum Voice
            </div>

            <div class="quantum-status">
                <span class="online-dot">●</span>
                Online • Voice Intelligence
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="voice-card">

            <h3>🎙️ Talk to Quantum AI</h3>

            <p class="small-status">
                Press the microphone button, speak, and Quantum AI
                will transcribe your voice and answer.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    audio = st.audio_input(
        "🎙️ Press to record"
    )

    if audio is not None:

        audio_hash = hashlib.md5(
            audio.getvalue()
        ).hexdigest()

        if audio_hash != st.session_state.last_voice_text:

            st.session_state.last_voice_text = audio_hash

            with st.spinner("Listening..."):

                try:

                    transcript = transcribe_audio(audio)

                    if not transcript:

                        st.warning(
                            "I couldn't hear anything. Please try again."
                        )

                    else:

                        st.markdown("### 🗣️ You")

                        st.write(transcript)

                        st.session_state.voice_messages.append(
                            {
                                "role": "user",
                                "content": transcript,
                            }
                        )

                        with st.spinner("Quantum AI is responding..."):

                            answer = ask_quantum_ai(
                                transcript,
                                st.session_state.voice_messages[:-1],
                            )

                        st.session_state.voice_messages.append(
                            {
                                "role": "assistant",
                                "content": answer,
                            }
                        )

                        st.markdown("### 🤖 Quantum AI")

                        st.markdown(answer)

                        st.markdown("### 🔊 Voice")

                        st.session_state.last_spoken_response = answer

                        speak_text(
                            answer,
                            autoplay=True,
                        )

                except Exception as e:

                    st.error(
                        f"Voice error: {str(e)}"
                    )


# ============================================================
# DIVISIONS
# ============================================================

elif page == "🏢 Divisions":

    st.markdown("# 🏢 Empire Divisions")

    divisions = [
        "🤖 AI",
        "🦾 Robotics",
        "⚡ Energy",
        "🧬 Health",
        "🚀 Space",
        "🏆 Sports",
        "🏭 Manufacturing",
        "🏗️ Infrastructure",
        "🛡️ Defense",
        "🧭 Exploration",
    ]

    for division in divisions:
        st.markdown(
            f"""
            <div style="
                background:rgba(255,255,255,0.04);
                padding:18px;
                margin:8px 0;
                border-radius:14px;
                border:1px solid rgba(255,255,255,0.06);
                font-size:18px;
            ">
                {division}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# FILES
# ============================================================

elif page == "📁 Files":

    st.markdown("# 📁 Files")

    uploaded_files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
    )

    if uploaded_files:

        for file in uploaded_files:

            st.write(
                f"📄 {file.name}"
            )


# ============================================================
# SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    st.markdown("# ⚙️ Settings")

    st.success("Groq API connection configured.")

    st.write(
        f"Chat model: `{CHAT_MODEL}`"
    )

    st.write(
        f"Speech recognition: `{VOICE_MODEL}`"
    )

    st.write(
        "Vision: Disabled"
    )

    st.divider()

    if st.button("🗑️ Clear Text Conversation"):

        st.session_state.messages = []

        st.rerun()

    if st.button("🗑️ Clear Voice Conversation"):

        st.session_state.voice_messages = []

        st.rerun()