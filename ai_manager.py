import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        # TEXT AI ONLY — NO VISION
        self.text_model = "qwen/qwen3.6-27b"

        # VOICE TRANSCRIPTION ONLY
        self.voice_model = "whisper-large-v3-turbo"

    # ==========================================
    # TEXT AI
    # ==========================================

    def text(self, prompt, history=None):

        messages = [
            {
                "role": "system",
                "content": """
You are Quantum AI, the central intelligence
of Quantum OS.

You are part of The Quantum Administration Empire.

The Empire includes:

AI
Robotics
Energy
Health
Space
Sports
Manufacturing
Infrastructure
Defense
Exploration

Be direct, useful and accurate.

Do not reveal internal reasoning.
Do not pretend hypothetical projects already exist.
"""
            }
        ]

        if history:
            messages.extend(history)

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model=self.text_model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )

        answer = response.choices[0].message.content

# Remove any visible reasoning blocks
if "<think>" in answer:
    answer = answer.split("<think>", 1)[1]
    if "</think>" in answer:
        answer = answer.split("</think>", 1)[1]

return answer.strip()

    # ==========================================
    # VOICE → TEXT
    # ==========================================

    def transcribe(self, audio_bytes):

        response = self.client.audio.transcriptions.create(
            file=(
                "quantum_voice.wav",
                audio_bytes,
                "audio/wav"
            ),
            model=self.voice_model,
            response_format="json"
        )

        return response.text

    # ==========================================
    # MODEL INFORMATION
    # ==========================================

    def get_models(self):

        return {
            "Text AI": self.text_model,
            "Voice": self.voice_model
        }