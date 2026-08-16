import streamlit as st
from ai_manager import QuantumAIManager


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Quantum AI",
    page_icon="⚛️",
    layout="wide"
)


# =========================================================
# AI MANAGER
# =========================================================

ai = QuantumAIManager()


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
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
        margin-bottom: 0px;
    }

    .quantum-subtitle {
        font-size: 18px;
        opacity: 0.7;
        margin-bottom: 30px;
    }

    .message-box {
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 14px;
    }

    .user-box {
        background: rgba(255,255,255,0.07);
    }

    .ai-box {
        background: rgba(80,100,200,0.12);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="quantum-title">🤖 Quantum AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="quantum-subtitle">Central intelligence system</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚛️ Quantum OS")

    st.markdown("### System")

    st.write("🏠 Home")
    st.write("🤖 Quantum AI")
    st.write("🏢 Divisions")
    st.write("📁 Files")
    st.write("⚙️ Settings")

    st.divider()

    st.markdown(
        "**The Quantum Administration Empire**"
    )

    st.caption("Quantum OS")


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    role = message["role"]
    content = message["content"]

    if role == "user":

        st.markdown(
            f"""
            <div class="message-box user-box">
                <strong>👤 You</strong>
                <br><br>
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="message-box ai-box">
                <strong>🤖 Quantum AI</strong>
                <br><br>
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_message = st.chat_input(
    "Ask Quantum AI..."
)


# =========================================================
# PROCESS MESSAGE
# =========================================================

if user_message:

    # Display/store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Prepare history for Groq
    history = []

    for message in st.session_state.messages[:-1]:

        history.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    try:

        answer = ai.chat(
            user_message,
            history
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as error:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content":
                    f"Quantum AI encountered an error:\n\n"
                    f"`{error}`"
            }
        )

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Quantum OS • The Quantum Administration Empire"
)