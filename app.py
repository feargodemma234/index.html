import streamlit as st
from ai_manager import QuantumAIManager


st.set_page_config(
    page_title="Quantum AI",
    page_icon="⚛️",
    layout="wide"
)


ai = QuantumAIManager()


if "messages" not in st.session_state:
    st.session_state.messages = []


# ==============================
# STYLE
# ==============================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top right,
            #18245c 0%,
            #080b16 45%,
            #05070d 100%
        );
}

.quantum-title {
    font-size: 52px;
    font-weight: 800;
}

.quantum-subtitle {
    font-size: 18px;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)


# ==============================
# HEADER
# ==============================

st.markdown(
    '<div class="quantum-title">🤖 Quantum AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="quantum-subtitle">'
    'Central intelligence system'
    '</div>',
    unsafe_allow_html=True
)


# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.title("⚛️ Quantum OS")

    st.write("🏠 Home")
    st.write("🤖 Quantum AI")
    st.write("🎤 Quantum Voice")
    st.write("🏢 Divisions")
    st.write("📁 Files")
    st.write("⚙️ Settings")

    st.divider()

    st.write("The Quantum Administration Empire")


# ==============================
# CHAT HISTORY
# ==============================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ==============================
# TEXT INPUT
# ==============================

prompt = st.chat_input("Ask Quantum AI...")


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    history = st.session_state.messages[:-1]

    with st.chat_message("assistant"):

        with st.spinner("Quantum AI is thinking..."):

            try:
                answer = ai.chat(
                    prompt,
                    history
                )

                st.write(answer)

                # Generate spoken response
                audio = ai.speak(answer)

                st.audio(
                    audio,
                    format="audio/wav"
                )

            except Exception as error:

                answer = f"Quantum AI encountered an error: {error}"

                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ==============================
# VOICE INPUT
# ==============================

st.divider()

st.subheader("🎤 Talk to Quantum AI")

audio_input = st.audio_input(
    "Record your message"
)


if audio_input:

    with st.spinner("Listening..."):

        try:

            spoken_text = ai.transcribe(
                audio_input
            )

            st.write(
                f"**You said:** {spoken_text}"
            )

            st.session_state.messages.append({
                "role": "user",
                "content": spoken_text
            })

            history = st.session_state.messages[:-1]

            with st.spinner("Quantum AI is thinking..."):

                answer = ai.chat(
                    spoken_text,
                    history
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.write(
                f"**🤖 Quantum AI:** {answer}"
            )

            # Speak answer
            audio = ai.speak(answer)

            st.audio(
                audio,
                format="audio/wav"
            )

        except Exception as error:

            st.error(
                f"Voice error: {error}"
            )


st.divider()

st.caption(
    "Quantum OS • The Quantum Administration Empire"
)