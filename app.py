import streamlit as st
import streamlit.components.v1 as components
from ai_manager import QuantumAIManager
import html


# ==================================================
# QUANTUM OS CONFIG
# ==================================================

st.set_page_config(
    page_title="Quantum OS",
    page_icon="⚛️",
    layout="wide"
)


# ==================================================
# AI MANAGER
# ==================================================

ai = QuantumAIManager()


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "vision_result" not in st.session_state:
    st.session_state.vision_result = ""


if "voice_result" not in st.session_state:
    st.session_state.voice_result = ""


# ==================================================
# STYLE
# ==================================================

st.markdown("""
<style>

.stApp {

    background:
        radial-gradient(
            circle at top right,
            #17245c,
            transparent 35%
        ),
        radial-gradient(
            circle at bottom left,
            #101d42,
            transparent 35%
        ),
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


.subtitle {

    color: #aeb8d8;
    font-size: 17px;
    margin-bottom: 25px;

}


.card {

    padding: 22px;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid rgba(255,255,255,0.08);

    margin-bottom: 16px;

}


.status {

    padding: 15px;

    border-radius: 15px;

    background:
        rgba(0,255,180,0.08);

    border:
        1px solid rgba(0,255,180,0.15);

}


</style>
""", unsafe_allow_html=True)


# ==================================================
# SPEAK FUNCTION
# ==================================================

def speak_response(text):

    safe_text = html.escape(text)

    components.html(
        f"""
        <script>

        const text = {safe_text!r};

        function speak() {{

            if (!("speechSynthesis" in window)) {{
                alert(
                    "Speech synthesis is not supported "
                    + "by this browser."
                );
                return;
            }}

            window.speechSynthesis.cancel();

            const utterance =
                new SpeechSynthesisUtterance(text);

            utterance.lang = "en-US";
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;

            window.speechSynthesis.speak(
                utterance
            );
        }}

        </script>

        <button
            onclick="speak()"
            style="
                width:100%;
                padding:14px;
                border-radius:12px;
                border:none;
                font-size:16px;
                cursor:pointer;
            "
        >
        🔊 Speak Quantum AI
        </button>
        """,
        height=65
    )


# ==================================================
# SIDEBAR
# ==================================================

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

    st.caption(
        "The Quantum Administration Empire"
    )

    st.caption(
        "Quantum OS v0.5"
    )


# ==================================================
# HOME
# ==================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="quantum-title">'
        '⚛️ Quantum OS'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'The digital foundation of '
        'The Quantum Administration Empire.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="card">

        <h3>🤖 Quantum AI</h3>

        <p>
        General artificial intelligence
        powered through the Quantum AI Manager.
        </p>

        </div>
        """, unsafe_allow_html=True)


    with col2:

        st.markdown("""
        <div class="card">

        <h3>🎙️ Quantum Voice</h3>

        <p>
        Talk to Quantum AI using your microphone.
        </p>

        </div>
        """, unsafe_allow_html=True)


    with col3:

        st.markdown("""
        <div class="card">
        </p>

        </div>
        """, unsafe_allow_html=True)


    st.divider()

    st.subheader("System Status")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Quantum OS",
            "ONLINE"
        )

    with c2:
        st.metric(
            "AI",
            "ONLINE"
        )

    with c4:
        st.metric(
            "VOICE",
            "ONLINE"
        )


# ==================================================
# TEXT AI
# ==================================================

elif page == "🤖 Quantum AI":

    st.title("🤖 Quantum AI")

    st.caption(
        "Central intelligence system"
    )


    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    prompt = st.chat_input(
        "Ask Quantum AI..."
    )


    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )


        with st.chat_message("user"):

            st.markdown(prompt)


        with st.chat_message("assistant"):

            with st.spinner(
                "Quantum AI is thinking..."
            ):

                try:

                    answer = ai.text(
                        prompt,
                        st.session_state.messages[
                            :-1
                        ]
                    )

                except Exception as e:

                    answer = (
                        "Quantum AI encountered "
                        "an error.\n\n"
                        f"`{e}`"
                    )


            st.markdown(answer)

            speak_response(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# ==================================================
# VOICE
# ==================================================

elif page == "🎙️ Quantum Voice":

    st.title("🎙️ Quantum Voice")

    st.write(
        "Speak to Quantum AI."
    )

    st.info(
        "Press the microphone button, speak, "
        "then stop recording."
    )


    audio = st.audio_input(
        "🎤 Record your message",
        sample_rate=16000
    )


    if audio:

        st.audio(
            audio
        )


        with st.spinner(
            "🎧 Transcribing..."
        ):

            try:

                user_text = ai.transcribe(
                    audio.getvalue()
                )

            except Exception as e:

                st.error(
                    f"Transcription error: {e}"
                )

                user_text = None


        if user_text:

            st.markdown(
                f"### 🧑 You\n{user_text}"
            )


            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_text
                }
            )


            with st.spinner(
                "🤖 Quantum AI is thinking..."
            ):

                try:

                    answer = ai.text(
                        user_text,
                        st.session_state.messages[
                            :-1
                        ]
                    )

                except Exception as e:

                    answer = (
                        "Quantum AI error:\n\n"
                        f"`{e}`"
                    )


            st.markdown(
                "### 🤖 Quantum AI"
            )

            st.write(answer)


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            st.divider()

            st.markdown(
                "### 🔊 Voice response"
            )

            speak_response(
                answer
            )


# ==================================================
# VISION
# ==================================================

elif page == "👁️ Quantum Vision":

    st.title("👁️ Quantum Vision")

    st.write(
        "Point your phone camera at something "
        "and ask Quantum Vision about it."
    )


    camera_image = st.camera_input(
        "📷 Take a picture"
    )


    if camera_image:

        st.image(
            camera_image,
            caption="Quantum Vision input",
            use_container_width=True
        )


        question = st.text_input(
            "What should Quantum Vision look for?",
            value=(
                "Identify the visible objects "
                "and describe what you see."
            )
        )


        if st.button(
            "👁️ Analyze Image",
            use_container_width=True
        ):

            with st.spinner(
                "👁️ Quantum Vision is analyzing..."
            ):

                try:

                    result = ai.vision(
                        question,
                        camera_image.getvalue()
                    )

                    st.session_state.vision_result = result

                except Exception as e:

                    st.session_state.vision_result = (
                        "Vision error:\n\n"
                        f"`{e}`"
                    )


    if st.session_state.vision_result:

        st.divider()

        st.subheader(
            "👁️ Quantum Vision Result"
        )

        st.write(
            st.session_state.vision_result
        )

        st.divider()

        st.markdown(
            "### 🔊 Speak result"
        )

        speak_response(
            st.session_state.vision_result
        )


# ==================================================
# DIVISIONS
# ==================================================

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

            <h2>
            {icon} Quantum {name}
            </h2>

            <p>
            Division allocation:
            <b>100 billion shares</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.metric(
        "Total Shares",
        "1,000,000,000,000"
    )


# ==================================================
# FILES
# ==================================================

elif page == "📁 Files":

    st.title(
        "📁 Quantum Files"
    )


    files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True
    )


    if files:

        for file in files:

            st.write(
                f"📄 {file.name}"
            )

            st.caption(
                f"{file.size:,} bytes"
            )


# ==================================================
# SETTINGS
# ==================================================

elif page == "⚙️ Settings":

    st.title(
        "⚙️ Quantum OS Settings"
    )


    st.write(
        "**Quantum OS:** v0.5"
    )

    st.write(
        "**AI Manager:** Active"
    )

    st.write(
        "**General Model:** "
        "Llama 4 Scout"
    )

    st.write(
        "**Vision Model:** "
        "Llama 4 Scout"
    )

    st.write(
        "**Speech Model:** "
        "Whisper Large V3 Turbo"
    )


    st.divider()


    st.subheader(
        "Current AI Models"
    )


    models = ai.get_models()


    for capability, model in models.items():

        st.write(
            f"**{capability}:** `{model}`"
        )


    st.divider()


    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.success(
            "Conversation cleared."
        )


    st.divider()


    st.caption(
        "Project: Building an Empire"
    )

    st.caption(
        "Organization: "
        "The Quantum Administration Empire"
    )