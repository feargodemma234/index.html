import base64
import streamlit as st
import streamlit.components.v1 as components

from ai_manager import QuantumAIManager


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Quantum AI",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# AI
# =========================================================

ai = QuantumAIManager()


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN APP ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 80% 0%,
                rgba(60, 80, 180, 0.25),
                transparent 35%
            ),
            radial-gradient(
                circle at 10% 20%,
                rgba(110, 50, 180, 0.15),
                transparent 30%
            ),
            #070914;
        color: white;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #090c18;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .sidebar-title {
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        color: #8d94aa;
        font-size: 13px;
        margin-bottom: 30px;
    }

    .nav-item {
        padding: 13px 15px;
        margin: 5px 0;
        border-radius: 12px;
        color: #c8ccda;
        font-size: 15px;
    }

    .nav-active {
        background: rgba(110, 120, 255, 0.18);
        color: white;
    }

    /* ---------- HEADER ---------- */

    .quantum-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 15px;
    }

    .quantum-logo {
        width: 58px;
        height: 58px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        background: linear-gradient(
            135deg,
            #6c63ff,
            #9b5cff
        );
        box-shadow:
            0 0 30px rgba(108,99,255,0.35);
    }

    .quantum-name {
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .quantum-status {
        color: #8e96aa;
        font-size: 14px;
    }

    /* ---------- WELCOME ---------- */

    .welcome {
        text-align: center;
        padding: 70px 20px 35px 20px;
    }

    .welcome-icon {
        font-size: 50px;
        margin-bottom: 10px;
    }

    .welcome-title {
        font-size: 30px;
        font-weight: 750;
    }

    .welcome-text {
        color: #8e96aa;
        font-size: 15px;
    }

    /* ---------- CHAT ---------- */

    .user-card {
        background: #151a2b;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 15px 18px;
        margin: 12px 0;
    }

    .assistant-card {
        background:
            linear-gradient(
                135deg,
                rgba(75,83,180,0.17),
                rgba(40,43,75,0.22)
            );
        border: 1px solid rgba(120,130,255,0.12);
        border-radius: 18px;
        padding: 18px;
        margin: 12px 0 25px 0;
    }

    .message-label {
        font-size: 12px;
        color: #8e96aa;
        margin-bottom: 7px;
    }

    /* ---------- VOICE ---------- */

    .voice-panel {
        background:
            linear-gradient(
                145deg,
                rgba(94,78,190,0.18),
                rgba(18,21,38,0.8)
            );
        border: 1px solid rgba(130,130,255,0.16);
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        margin-top: 25px;
    }

    .voice-icon {
        font-size: 42px;
    }

    .voice-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 8px;
    }

    .voice-text {
        color: #8e96aa;
        font-size: 14px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #555d72;
        font-size: 12px;
        padding: 30px;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 700px) {

        .quantum-name {
            font-size: 30px;
        }

        .welcome {
            padding-top: 40px;
        }

        .quantum-header {
            margin-top: 5px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚛️ Quantum OS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Quantum Administration Empire'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item nav-active">🤖 Quantum AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">🏠 Home</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">🎤 Quantum Voice</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">🏢 Divisions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">📁 Files</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">⚙️ Settings</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("Quantum OS")
    st.caption("AI • Voice • Intelligence")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="quantum-header">
        <div class="quantum-logo">⚛️</div>
        <div>
            <div class="quantum-name">Quantum AI</div>
            <div class="quantum-status">
                ● Online • Central Intelligence
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome">

            <div class="welcome-icon">🤖</div>

            <div class="welcome-title">
                How can I help?
            </div>

            <div class="welcome-text">
                Talk to Quantum AI or type a message below.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-card">
                <div class="message-label">YOU</div>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-card">
                <div class="message-label">⚛️ QUANTUM AI</div>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# VOICE PANEL
# =========================================================

st.markdown(
    """
    <div class="voice-panel">

        <div class="voice-icon">🎤</div>

        <div class="voice-title">
            Talk to Quantum AI
        </div>

        <div class="voice-text">
            Tap the microphone, speak, and Quantum AI will respond.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MICROPHONE
# =========================================================

audio = st.audio_input(
    "🎤 Tap to speak"
)


if audio:

    # -------------------------
    # SPEECH TO TEXT
    # -------------------------

    with st.spinner("🎧 Listening..."):

        try:

            user_text = ai.transcribe(
                audio.getvalue()
            )

        except Exception as e:

            st.error(
                f"Voice input error: {e}"
            )

            user_text = None


    if user_text:

        st.markdown(
            f"""
            <div class="user-card">
                <div class="message-label">YOU SAID</div>
                {user_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_text
            }
        )


        # -------------------------
        # AI
        # -------------------------

        history = st.session_state.messages[:-1]

        with st.spinner("⚛️ Quantum AI is thinking..."):

            try:

                answer = ai.chat(
                    user_text,
                    history
                )

            except Exception as e:

                st.error(
                    f"AI error: {e}"
                )

                answer = None


        if answer:

            st.markdown(
                f"""
                <div class="assistant-card">
                    <div class="message-label">
                        ⚛️ QUANTUM AI
                    </div>
                    {answer}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            # -------------------------
            # TEXT TO SPEECH
            # -------------------------

            with st.spinner("🔊 Quantum AI is speaking..."):

                try:

                    audio_data = ai.speak(
                        answer
                    )

                    encoded = base64.b64encode(
                        audio_data
                    ).decode("utf-8")


                    components.html(
                        f"""
                        <audio
                            id="quantumVoice"
                            autoplay
                            controls
                            style="
                                width:100%;
                                border-radius:12px;
                            "
                        >
                            <source
                                src="data:audio/wav;base64,{encoded}"
                                type="audio/wav"
                            >
                        </audio>

                        <script>

                        const audio =
                            document.getElementById(
                                "quantumVoice"
                            );

                        audio.play().catch(
                            function(error) {{
                                console.log(
                                    "Browser blocked autoplay"
                                );
                            }}
                        );

                        </script>
                        """,
                        height=70
                    )

                except Exception as e:

                    st.error(
                        f"Voice output error: {e}"
                    )


# =========================================================
# TEXT INPUT
# =========================================================

prompt = st.chat_input(
    "Message Quantum AI..."
)


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    history = st.session_state.messages[:-1]

    with st.spinner("⚛️ Thinking..."):

        try:

            answer = ai.chat(
                prompt,
                history
            )

        except Exception as e:

            answer = f"AI error: {e}"


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Quantum OS • Quantum Administration Empire
        <br>
        AI Intelligence System
    </div>
    """,
    unsafe_allow_html=True
)