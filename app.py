import streamlit as st
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="Quantum OS",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# QUANTUM OS STYLE
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

section[data-testid="stSidebar"] {
    background: #0b1020;
}

h1, h2, h3 {
    color: white;
}

.quantum-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.quantum-subtitle {
    color: #aeb8d8;
    font-size: 16px;
}

.card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
}

.division {
    padding: 18px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    min-height: 120px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# SESSION STATE
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


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
            "🏢 Divisions",
            "📁 Files",
            "⚙️ Settings"
        ]
    )

    st.divider()

    st.caption("Quantum Administration Empire")
    st.caption("Quantum OS v0.2")


# -----------------------------
# HOME
# -----------------------------

if page == "🏠 Home":

    st.markdown(
        '<div class="quantum-title">⚛️ Quantum OS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="quantum-subtitle">'
        'The digital foundation of The Quantum Administration Empire.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="card">'
            '<h3>🤖 Quantum AI</h3>'
            '<p>AI intelligence powered by Groq.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="card">'
            '<h3>🏢 Empire</h3>'
            '<p>10 major technology and industrial divisions.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="card">'
            '<h3>⚡ System</h3>'
            '<p>Quantum OS v0.2 prototype.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    st.subheader("Empire Overview")

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

    cols = st.columns(5)

    for i, (icon, name) in enumerate(divisions):

        with cols[i % 5]:

            st.markdown(
                f'''
                <div class="division">
                    <h3>{icon} {name}</h3>
                    <p>Quantum {name} Division</p>
                </div>
                ''',
                unsafe_allow_html=True
            )


# -----------------------------
# QUANTUM AI
# -----------------------------

elif page == "🤖 Quantum AI":

    st.title("🤖 Quantum AI")

    st.caption("Powered by Groq")

    # Display conversation
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
You are Quantum AI, the AI assistant
inside Quantum OS.

You are part of The Quantum Administration Empire.

Be helpful, clear, ambitious, and technically accurate.
Help users design software, AI systems,
businesses, robotics, infrastructure,
and other technology projects.

Do not claim that fictional projects already exist.
Distinguish plans from real-world facts.
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
                "Quantum AI could not connect to Groq.\n\n"
                "Check your GROQ_API_KEY in Streamlit Secrets.\n\n"
                f"Error: `{e}`"
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.markdown(answer)


# -----------------------------
# DIVISIONS
# -----------------------------

elif page == "🏢 Divisions":

    st.title("🏢 Quantum Administration Empire")

    st.write(
        "The empire currently consists of 10 equal divisions."
    )

    divisions = [
        ("🤖", "AI", "100 billion shares"),
        ("🦾", "Robotics", "100 billion shares"),
        ("⚡", "Energy", "100 billion shares"),
        ("🧬", "Health", "100 billion shares"),
        ("🚀", "Space", "100 billion shares"),
        ("🏆", "Sports", "100 billion shares"),
        ("🏭", "Manufacturing", "100 billion shares"),
        ("🏗️", "Infrastructure", "100 billion shares"),
        ("🛡️", "Defense", "100 billion shares"),
        ("🌌", "Exploration", "100 billion shares")
    ]

    for icon, name, shares in divisions:

        st.markdown(
            f"""
            <div class="card">
                <h2>{icon} Quantum {name}</h2>
                <p>Division allocation: {shares}</p>
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

    uploaded = st.file_uploader(
        "Upload a file",
        accept_multiple_files=True
    )

    if uploaded:

        st.success(
            f"{len(uploaded)} file(s) uploaded."
        )

        for file in uploaded:

            st.write(
                f"📄 {file.name}"
            )


# -----------------------------
# SETTINGS
# -----------------------------

elif page == "⚙️ Settings":

    st.title("⚙️ Quantum OS Settings")

    st.write("### System Information")

    st.write("**Operating System:** Quantum OS")
    st.write("**Version:** 0.2")
    st.write("**AI Engine:** Groq")
    st.write("**Interface:** Streamlit")
    st.write("**Project:** Building an Empire")

    st.divider()

    if st.button("Clear AI Conversation"):

        st.session_state.messages = []

        st.success(
            "Quantum AI conversation cleared."
        )

    st.divider()

    st.caption(
        f"System time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )