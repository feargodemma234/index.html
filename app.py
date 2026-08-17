import streamlit as st
from ai_manager import QuantumAIManager

st.set_page_config(
    page_title="Quantum OS",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# STYLING
# -----------------------------

st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at top right, #18245c 0%, #080b18 45%, #050711 100%);
        color: white;
    }

    [data-testid="stSidebar"] {
        background: #080b18;
    }

    .quantum-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .quantum-subtitle {
        color: #aeb5c8;
        font-size: 17px;
        margin-top: 0;
    }

    .welcome {
        padding: 35px;
        border-radius: 25px;
        background: rgba(25, 29, 48, 0.85);
        border: 1px solid rgba(130, 110, 255, 0.25);
        margin-top: 25px;
    }

    .status {
        color: #9ea6bc;
        font-size: 16px;
    }

    .ai-message {
        padding: 20px;
        border-radius: 18px;
        background: rgba(25, 29, 48, 0.9);
        margin: 10px 0;
    }

    .user-message {
        padding: 18px;
        border-radius: 18px;
        background: rgba(77, 55, 145, 0.35);
        margin: 10px 0;
    }

    .section-card {
        padding: 25px;
        border-radius: 22px;
        background: rgba(20, 24, 42, 0.85);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SESSION STATE
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ai" not in st.session_state:
    st.session_state.ai = QuantumAIManager()


ai = st.session_state.ai


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("# ⚛️ Quantum OS")
    st.caption("The Quantum Administration Empire")

    st.divider()

    page = st.radio(
        "System",
        [
            "🏠 Home",
            "🤖 Quantum AI",
            "🎙️ Quantum Voice",
            "🏢 Divisions",
            "📁 Files",
            "⚙️ Settings",
        ],
    )

    st.divider()

    st.caption("Quantum OS")
    st.caption("Version 1.0")


# -----------------------------
# HOME
# -----------------------------

if page == "🏠 Home":

    st.markdown(
        '<div class="quantum-title">⚛️ Quantum OS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="quantum-subtitle">Central administration system</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="welcome">
        <h2>Welcome to Quantum OS</h2>
        <p>
        Quantum OS is the central platform for the Quantum Administration Empire.
        </p>
        <p>
        Use the sidebar to access Quantum AI, Quantum Voice,
        divisions, files and system settings.
        </p>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# TEXT AI
# -----------------------------

elif page == "🤖 Quantum AI":

    st.markdown(
        '<div class="quantum-title">🤖 Quantum AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="quantum-subtitle">Direct text conversation</div>',
        unsafe_allow_html=True
    )

    st.divider()

    for message in st.session_state.messages:

        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="user-message">
                    <b>You</b><br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div class="ai-message">
                    <b>⚛️ Quantum AI</b><br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    prompt = st.chat_input("Message Quantum AI...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.spinner("Quantum AI is thinking..."):

            try:
                answer = ai.chat(st.session_state.messages)

            except Exception as e:
                answer = f"Quantum AI error: {e}"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()


# -----------------------------
# VOICE
# -----------------------------

elif page == "🎙️ Quantum Voice":

    st.markdown(
        '<div class="quantum-title">🎙️ Quantum Voice</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="quantum-subtitle">Speak to Quantum AI and hear the response</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="section-card">'
        '<h3>🎙️ Speak</h3>'
        '<p>Record your question below.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    audio = st.audio_input(
        "Press the microphone button and speak"
    )

    if audio is not None:

        with st.spinner("Listening..."):

            try:
                text = ai.transcribe(audio)

            except Exception as e:
                st.error(f"Speech recognition error: {e}")
                text = None

        if text:

            st.markdown("### You said")

            st.info(text)

            with st.spinner("Quantum AI is thinking..."):

                try:
                    answer = ai.chat(
                        [
                            {
                                "role": "user",
                                "content": text
                            }
                        ]
                    )

                except Exception as e:
                    st.error(f"AI error: {e}")
                    answer = None

            if answer:

                st.markdown("### ⚛️ Quantum AI")

                st.write(answer)

                with st.spinner("Generating voice..."):

                    try:
                        audio_bytes = ai.text_to_speech(answer)

                        if audio_bytes:
                            st.audio(
                                audio_bytes,
                                format="audio/wav"
                            )

                    except Exception as e:
                        st.error(f"Voice error: {e}")


# -----------------------------
# DIVISIONS
# -----------------------------

elif page == "🏢 Divisions":

    st.markdown(
        '<div class="quantum-title">🏢 Divisions</div>',
        unsafe_allow_html=True
    )

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
        "🌍 Exploration",
    ]

    for division in divisions:
        st.markdown(
            f"""
            <div class="section-card">
                <h3>{division}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# FILES
# -----------------------------

elif page == "📁 Files":

    st.markdown(
        '<div class="quantum-title">📁 Files</div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "Upload a file",
        accept_multiple_files=True
    )

    if uploaded:

        for file in uploaded:
            st.success(f"Loaded: {file.name}")


# -----------------------------
# SETTINGS
# -----------------------------

elif page == "⚙️ Settings":

    st.markdown(
        '<div class="quantum-title">⚙️ Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="section-card">
        <h3>Quantum OS Settings</h3>
        <p>AI Model: OpenAI GPT-OSS 20B</p>
        <p>Speech Recognition: Whisper Large V3 Turbo</p>
        <p>Voice: Groq Orpheus</p>
        <p>Vision: Disabled</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear conversation"):

        st.session_state.messages = []

        st.success("Conversation cleared.")

        st.rerun()