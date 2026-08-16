import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
from datetime import datetime

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Quantum OS",
    page_icon="⚛️",
    layout="wide"
)

# ==============================
# STYLE
# ==============================

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

h1, h2, h3 {
    color: white;
}

.quantum-title {
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    color: #aeb8d8;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
}

.voice-card {
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.markdown("## ⚛️ Quantum OS")

    page = st.radio(
        "System",
        [
            "🏠 Home",
            "🤖 Quantum AI",
            "🎙️ Voice AI",
            "🏢 Divisions",
            "📁 Files",
            "⚙️ Settings"
        ]
    )

    st.divider()

    st.caption("The Quantum Administration Empire")
    st.caption("Quantum OS v0.3")


# ==============================
# HOME
# ==============================

if page == "🏠 Home":

    st.markdown(
        '<div class="quantum-title">⚛️ Quantum OS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'The digital foundation of The Quantum Administration Empire.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🤖 Quantum AI</h3>
        <p>AI intelligence powered by Groq.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>🎙️ Voice</h3>
        <p>Talk to Quantum AI using your microphone.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>🏢 Empire</h3>
        <p>10 major divisions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("System Status")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Quantum OS", "ONLINE")

    with c2:
        st.metric("AI Engine", "GROQ")

    with c3:
        st.metric("Version", "0.3")


# ==============================
# TEXT AI
# ==============================

elif page == "🤖 Quantum AI":

    st.title("🤖 Quantum AI")

    st.caption("Powered by Groq")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask Quantum AI...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        try:

            client = Groq(
                api_key=st.secrets["GROQ_API_KEY"]
            )

            messages = [
                {
                    "role": "system",
                    "content": """
You are Quantum AI.

You are the AI assistant of
The Quantum Administration Empire.

Help the user build technology,
software, AI, robotics, energy,
health, space, manufacturing,
infrastructure and exploration projects.

Be clear, ambitious and technically
accurate.

Never pretend that a hypothetical
project already exists.
"""
                }
            ]

            messages.extend(
                st.session_state.messages
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )

            answer = response.choices[0].message.content

        except Exception as e:

            answer = (
                "I couldn't connect to Groq.\n\n"
                "Check your GROQ_API_KEY in Streamlit Secrets.\n\n"
                f"Error: `{e}`"
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.markdown(answer)


# ==============================
# VOICE AI
# ==============================

elif page == "🎙️ Voice AI":

    st.title("🎙️ Quantum Voice")

    st.write(
        "Talk to Quantum AI using your device microphone."
    )

    st.divider()

    # Browser speech recognition
    components.html(
        """
        <!DOCTYPE html>

        <html>

        <body style="
            background: transparent;
            color: white;
            font-family: Arial;
            text-align: center;
        ">

        <h2>🎙️ Quantum Voice</h2>

        <button
            onclick="startListening()"
            style="
                font-size:20px;
                padding:15px 25px;
                border-radius:15px;
                border:none;
                cursor:pointer;
            "
        >
        🎤 Talk
        </button>

        <button
            onclick="stopSpeaking()"
            style="
                font-size:20px;
                padding:15px 25px;
                border-radius:15px;
                border:none;
                cursor:pointer;
                margin-left:10px;
            "
        >
        🔇 Stop
        </button>

        <p id="status">
        Press Talk and speak.
        </p>

        <p id="result"></p>

        <script>

        const SpeechRecognition =
            window.SpeechRecognition ||
            window.webkitSpeechRecognition;

        let recognition;

        if (SpeechRecognition) {

            recognition = new SpeechRecognition();

            recognition.continuous = false;

            recognition.interimResults = false;

            recognition.lang = "en-US";

            recognition.onstart = function() {

                document.getElementById("status")
                .innerText =
                "🎙️ Listening...";

            };

            recognition.onresult = function(event) {

                const text =
                    event.results[0][0].transcript;

                document.getElementById("result")
                .innerText =
                    "You said: " + text;

                document.getElementById("status")
                .innerText =
                    "Voice captured.";

                // Send recognized text to Streamlit
                window.parent.postMessage({
                    type: "quantum_voice",
                    text: text
                }, "*");

            };

            recognition.onerror = function(event) {

                document.getElementById("status")
                .innerText =
                    "Microphone error: " +
                    event.error;

            };

        } else {

            document.getElementById("status")
            .innerText =
            "Speech recognition is not supported by this browser.";

        }


        function startListening() {

            if (recognition) {

                recognition.start();

            }

        }


        function stopSpeaking() {

            window.speechSynthesis.cancel();

            document.getElementById("status")
            .innerText =
            "Speech stopped.";

        }

        </script>

        </body>

        </html>
        """,
        height=300
    )

    st.info(
        "The microphone component captures your voice. "
        "The next step is connecting the captured text "
        "directly to the Groq conversation."
    )


# ==============================
# DIVISIONS
# ==============================

elif page == "🏢 Divisions":

    st.title("🏢 Quantum Administration Empire")

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


# ==============================
# FILES
# ==============================

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


# ==============================
# SETTINGS
# ==============================

elif page == "⚙️ Settings":

    st.title("⚙️ Quantum OS Settings")

    st.write("**Version:** 0.3")
    st.write("**AI:** Groq")
    st.write("**Interface:** Streamlit")
    st.write("**Project:** Building an Empire")

    st.divider()

    if st.button("Clear AI Conversation"):

        st.session_state.messages = []

        st.success(
            "Conversation cleared."
        )

    st.divider()

    st.caption(
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )