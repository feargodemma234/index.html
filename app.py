from ai_manager import QuantumAIManager
ai = QuantumAIManager()
import streamlit as st
from groq import Groq
import base64
import html

st.set_page_config(
    page_title="Quantum OS",
    page_icon="⚛️",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# STYLING
# -----------------------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top right, #17245c, transparent 35%),
        radial-gradient(circle at bottom left, #101d42, transparent 35%),
        #080b14;
    color: white;
}

[data-testid="stSidebar"] {
    background: #090d1c;
}

.quantum-title {
    font-size: 42px;
    font-weight: 800;
}

.card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# GROQ
# -----------------------------

def get_groq():

    return Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )


# -----------------------------
# AI FUNCTION
# -----------------------------

def ask_quantum_ai(user_text):

    client = get_groq()

    system_prompt = """
You are Quantum AI, the AI assistant inside Quantum OS.

You are part of The Quantum Administration Empire.

Help the user with:
AI, software, robotics, energy, health,
space, sports, manufacturing,
infrastructure, defense, and exploration.

Be helpful, concise, technically accurate,
and clear.

The Quantum Administration Empire is a
project being developed by the user.
Do not claim that hypothetical projects
already exist.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(st.session_state.messages)

    messages.append({
        "role": "user",
        "content": user_text
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1500
    )

    return response.choices[0].message.content


# -----------------------------
# SPEAK RESPONSE
# -----------------------------

def speak_text(text):

    safe_text = html.escape(text)

    components_html = f"""
    <script>

    const text = {safe_text!r};

    if ("speechSynthesis" in window) {{

        window.speechSynthesis.cancel();

        const speech =
            new SpeechSynthesisUtterance(text);

        speech.lang = "en-US";
        speech.rate = 1.0;
        speech.pitch = 1.0;
        speech.volume = 1.0;

        window.speechSynthesis.speak(speech);
    }}

    </script>
    """

    st.components.v1.html(
        components_html,
        height=0
    )


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("## ⚛️ Quantum OS")

    page = st.radio(
        "System",
        [
            "🏠 Home",
            "🤖 Quantum AI",
            "🎙️ Quantum Voice",
            "🏢 Divisions",
            "📁 Files",
            "⚙️ Settings"
        ]
    )

    st.divider()

    st.caption("The Quantum Administration Empire")
    st.caption("Quantum OS v0.4")


# -----------------------------
# HOME
# -----------------------------

if page == "🏠 Home":

    st.markdown(
        '<div class="quantum-title">⚛️ Quantum OS</div>',
        unsafe_allow_html=True
    )

    st.write(
        "The digital foundation of "
        "The Quantum Administration Empire."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div class="card">
        <h3>🤖 Quantum AI</h3>
        <p>AI intelligence powered by Groq.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="card">
        <h3>🎙️ Quantum Voice</h3>
        <p>Talk to Quantum AI.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="card">
        <h3>🏢 Empire</h3>
        <p>10 major divisions.</p>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# TEXT AI
# -----------------------------

elif page == "🤖 Quantum AI":

    st.title("🤖 Quantum AI")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask Quantum AI..."
    )

    if prompt:

        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        try:

            answer = ask_quantum_ai(prompt)

        except Exception as e:

            answer = (
                "I couldn't connect to Groq.\n\n"
                f"Error: `{e}`"
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.markdown(answer)


# -----------------------------
# VOICE AI
# -----------------------------

elif page == "🎙️ Quantum Voice":

    st.title("🎙️ Quantum Voice")

    st.write(
        "Record your voice, and Quantum AI will "
        "answer aloud."
    )

    st.divider()

    audio = st.audio_input(
        "🎤 Press to record",
        sample_rate=16000,
        key="quantum_voice_input"
    )

    if audio:

        st.audio(audio)

        with st.spinner(
            "🎧 Understanding your voice..."
        ):

            try:

                client = get_groq()

                # Send audio to Groq transcription
                transcription = client.audio.transcriptions.create(
                    file=(
                        "voice.wav",
                        audio.getvalue(),
                        "audio/wav"
                    ),
                    model="whisper-large-v3-turbo"
                )

                user_text = transcription.text

                st.markdown(
                    f"**You:** {user_text}"
                )

                # Ask Quantum AI
                with st.spinner(
                    "🤖 Quantum AI is thinking..."
                ):

                    answer = ask_quantum_ai(
                        user_text
                    )

                st.markdown(
                    f"**Quantum AI:** {answer}"
                )

                # Save conversation
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_text
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                # Speak
                speak_text(answer)

                st.success(
                    "🔊 Quantum AI is speaking."
                )

            except Exception as e:

                st.error(
                    "Voice AI error:"
                )

                st.code(str(e))


# -----------------------------
# DIVISIONS
# -----------------------------

elif page == "🏢 Divisions":

    st.title(
        "🏢 Quantum Administration Empire"
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
        ("🌌", "Exploration")
    ]

    for icon, name in divisions:

        st.markdown(
            f"""
            <div class="card">
            <h2>{icon} Quantum {name}</h2>
            <p>Allocation: 100 billion shares</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.metric(
        "Total Shares",
        "1,000,000,000,000"
    )


# -----------------------------
# FILES
# -----------------------------

elif page == "📁 Files":

    st.title("📁 Quantum Files")

    files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True
    )

    if files:

        for file in files:

            st.write(
                f"📄 {file.name}"
            )


# -----------------------------
# SETTINGS
# -----------------------------

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.write(
        "**Quantum OS:** 0.4"
    )

    st.write(
        "**AI Engine:** Groq"
    )

    st.write(
        "**Voice:** Groq Whisper + Browser Speech"
    )

    st.write(
        "**Project:** Building an Empire"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation"
    ):

        st.session_state.messages = []

        st.success(
            "Conversation cleared."
        )