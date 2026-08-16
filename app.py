import base64
import streamlit as st
import streamlit.components.v1 as components

from ai_manager import QuantumAIManager


# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="Quantum AI",
    page_icon="⚛️",
    layout="centered"
)


# ==================================================
# AI
# ==================================================

ai = QuantumAIManager()


# ==================================================
# SESSION
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# UI
# ==================================================

st.title("⚛️ Quantum AI")

st.caption(
    "Talk to Quantum AI"
)

st.divider()


# ==================================================
# CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ==================================================
# VOICE INPUT
# ==================================================

st.subheader("🎤 Talk")

audio = st.audio_input(
    "Tap the microphone and speak"
)


if audio:

    with st.spinner("Listening..."):

        try:
            user_text = ai.transcribe(
                audio.getvalue()
            )

        except Exception as e:

            st.error(
                f"Speech recognition error: {e}"
            )

            user_text = None


    if user_text:

        st.chat_message(
            "user"
        ).write(user_text)

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_text
        })


        # Previous conversation
        history = st.session_state.messages[:-1]


        # ==========================================
        # AI RESPONSE
        # ==========================================

        with st.spinner(
            "Quantum AI is thinking..."
        ):

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

            st.chat_message(
                "assistant"
            ).write(answer)


            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })


            # ======================================
            # TEXT TO SPEECH
            # ======================================

            with st.spinner(
                "Quantum AI is speaking..."
            ):

                try:

                    audio_data = ai.speak(
                        answer
                    )

                    audio_base64 = base64.b64encode(
                        audio_data
                    ).decode("utf-8")


                    # Browser audio player
                    components.html(
                        f"""
                        <audio
                            id="quantumAudio"
                            autoplay
                            controls
                            style="width:100%;"
                        >
                            <source
                                src="data:audio/wav;base64,{audio_base64}"
                                type="audio/wav"
                            >
                        </audio>

                        <script>
                            const audio =
                                document.getElementById(
                                    "quantumAudio"
                                );

                            audio.play().catch(
                                function(error) {{
                                    console.log(
                                        "Autoplay blocked:",
                                        error
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


# ==================================================
# TEXT CHAT
# ==================================================

st.divider()

st.subheader("⌨️ Or type")


prompt = st.chat_input(
    "Ask Quantum AI..."
)


if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    history = st.session_state.messages[:-1]

    with st.spinner(
        "Quantum AI is thinking..."
    ):

        try:

            answer = ai.chat(
                prompt,
                history
            )

        except Exception as e:

            answer = (
                f"AI error: {e}"
            )


    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Quantum OS • The Quantum Administration Empire"
)

st.caption(
    "Voice AI • No Vision"
)