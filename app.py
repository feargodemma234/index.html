import base64
import streamlit as st
import streamlit.components.v1 as components

from ai_manager import QuantumAIManager


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Quantum OS",
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

if "page" not in st.session_state:
    st.session_state.page = "Text AI"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(90, 70, 220, 0.25),
            transparent 35%
        ),
        #070914;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #090c18;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
}

.sidebar-subtitle {
    color: #8b93a8;
    font-size: 13px;
}

/* Main title */

.quantum-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.quantum-status {
    color: #8d95aa;
    font-size: 14px;
}

/* Welcome */

.welcome-box {
    text-align: center;
    padding: 70px 20px;
}

.welcome-icon {
    font-size: 55px;
}

.welcome-title {
    font-size: 30px;
    font-weight: 800;
}

.welcome-description {
    color: #8d95aa;
}

/* Voice */

.voice-box {
    text-align: center;
    padding: 70px 20px;
    border-radius: 25px;
    background: rgba(70, 70, 150, 0.12);
    border: 1px solid rgba(130, 130, 255, 0.15);
}

.voice-icon {
    font-size: 70px;
}

.voice-title {
    font-size: 30px;
    font-weight: 800;
}

.voice-description {
    color: #8d95aa;
}

/* Footer */

.footer {
    text-align: center;
    color: #555d72;
    padding: 35px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


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

    st.divider()

    # Navigation
    selected_page = st.radio(
        "System",
        [
            "🏠 Home",
            "💬 Text AI",
            "🎤 Voice AI",
            "🏢 Divisions",
            "📁 Files",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )

    # Convert sidebar selection
    if "Text AI" in selected_page:
        st.session_state.page = "Text AI"

    elif "Voice AI" in selected_page:
        st.session_state.page = "Voice AI"

    elif "Home" in selected_page:
        st.session_state.page = "Home"

    elif "Divisions" in selected_page:
        st.session_state.page = "Divisions"

    elif "Files" in selected_page:
        st.session_state.page = "Files"

    elif "Settings" in selected_page:
        st.session_state.page = "Settings"

    st.divider()

    st.caption("Quantum OS")
    st.caption("AI • Voice • Intelligence")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="quantum-title">⚛️ Quantum AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="quantum-status">'
    '● Online • Central Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.markdown(
        '<div class="welcome-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-icon">⚛️</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-title">'
        'Welcome to Quantum OS'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-description">'
        'Choose Text AI or Voice AI from the sidebar.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "💬 **Text AI**\n\n"
            "Chat with Quantum AI using your keyboard."
        )

    with col2:
        st.info(
            "🎤 **Voice AI**\n\n"
            "Speak to Quantum AI and hear its response."
        )


# =========================================================
# TEXT AI
# =========================================================

elif st.session_state.page == "Text AI":

    st.subheader("💬 Text AI")

    st.caption(
        "Type a message and Quantum AI will respond."
    )

    # Display chat
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Message Quantum AI..."
    )

    if prompt:

        # User message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        # History before current message
        history = st.session_state.messages[:-1]

        # AI response
        with st.chat_message("assistant"):

            with st.spinner(
                "Quantum AI is thinking..."
            ):

                try:

                    answer = ai.chat(
                        prompt,
                        history
                    )

                    st.write(answer)

                except Exception as e:

                    answer = (
                        "Quantum AI encountered an error."
                    )

                    st.error(
                        f"{answer}\n\n{e}"
                    )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })


# =========================================================
# VOICE AI
# =========================================================

elif st.session_state.page == "Voice AI":

    st.markdown(
        '<div class="voice-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="voice-icon">🎤</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="voice-title">'
        'Quantum Voice'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="voice-description">'
        'Speak to Quantum AI and hear the response.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # Microphone
    audio = st.audio_input(
        "🎤 Tap here to speak"
    )

    if audio:

        # -----------------------------------------
        # TRANSCRIBE
        # -----------------------------------------

        with st.spinner(
            "🎧 Listening..."
        ):

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

            st.success(
                f"You said: {user_text}"
            )

            # -------------------------------------
            # AI
            # -------------------------------------

            with st.spinner(
                "⚛️ Quantum AI is thinking..."
            ):

                try:

                    answer = ai.chat(
                        user_text,
                        []
                    )

                except Exception as e:

                    st.error(
                        f"AI error: {e}"
                    )

                    answer = None


            if answer:

                st.write("### ⚛️ Quantum AI")

                st.write(answer)

                # ---------------------------------
                # TEXT TO SPEECH
                # ---------------------------------

                with st.spinner(
                    "🔊 Quantum AI is speaking..."
                ):

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
                                controls
                                autoplay
                                style="
                                    width:100%;
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
                                function() {{
                                    console.log(
                                        "Autoplay blocked by browser"
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
# DIVISIONS
# =========================================================

elif st.session_state.page == "Divisions":

    st.subheader("🏢 Quantum Administration Empire")

    divisions = [
        "🤖 AI",
        "🦾 Robotics",
        "⚡ Energy",
        "🏥 Health",
        "🚀 Space",
        "🏆 Sports",
        "🏭 Manufacturing",
        "🏗️ Infrastructure",
        "🛡️ Defense",
        "🌎 Exploration"
    ]

    for division in divisions:
        st.write(division)


# =========================================================
# FILES
# =========================================================

elif st.session_state.page == "Files":

    st.subheader("📁 Files")

    st.info(
        "File management can be added here."
    )


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":

    st.subheader("⚙️ Settings")

    st.write(
        "Quantum OS settings"
    )

    if st.button("Clear conversation"):

        st.session_state.messages = []

        st.success(
            "Conversation cleared."
        )

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'Quantum OS • Quantum Administration Empire'
    '</div>',
    unsafe_allow_html=True
)