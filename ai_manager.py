import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        self.models = {
            "text": "qwen/qwen3.6-27b",
            "speech_to_text": "whisper-large-v3-turbo"
        }

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

The Empire is being developed across:

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

You can help with:
- Programming
- Science
- Engineering
- Business
- Planning
- Research
- Mathematics
- Technology
- The development of Quantum OS

Be clear, useful and accurate.

Never claim that a hypothetical project
already exists when it does not.
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
            model=self.models["text"],
            messages=messages,
            temperature=0.7,
            max_tokens=3000
        )

        return response.choices[0].message.content

    # ==========================================
    # SPEECH TO TEXT
    # ==========================================

    def transcribe(self, audio_bytes):

        response = self.client.audio.transcriptions.create(
            file=(
                "quantum_voice.wav",
                audio_bytes,
                "audio/wav"
            ),
            model=self.models["speech_to_text"],
            response_format="json"
        )

        return response.text

    # ==========================================
    # MODEL INFORMATION
    # ==========================================

    def get_models(self):
        return self.models.copy()

    # ==========================================
    # CHANGE MODEL
    # ==========================================

    def set_model(self, capability, model):

        if capability not in self.models:
            raise ValueError(
                f"Unknown capability: {capability}"
            )

        self.models[capability] = model