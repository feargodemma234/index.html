import streamlit as st
from groq import Groq
import base64


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        self.models = {
    "general": "llama-3.3-70b-versatile",   # was llama-4-scout
    "vision": "llama-3.2-11b-vision-preview",  # Groq's current vision model
    "speech_to_text": "whisper-large-v3-turbo"  # this one is still good
}

    # ==========================================
    # GENERAL AI
    # ==========================================

    def text(self, prompt, history=None):

        system = """
You are Quantum AI, the central AI assistant
inside Quantum OS.

You are part of The Quantum Administration Empire.

Help with:
AI, software, robotics, energy, health,
space, sports, manufacturing,
infrastructure, defense, exploration,
business and scientific projects.

Be helpful, clear, technically accurate,
and honest about uncertainty.

The Quantum Administration Empire is a
project being developed by the user.

Do not claim hypothetical projects already exist.
"""

        messages = [
            {
                "role": "system",
                "content": system
            }
        ]

        if history:
            messages.extend(history)

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model=self.models["general"],
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content

    # ==========================================
    # VISION
    # ==========================================

    def vision(self, prompt, image_bytes):

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        response = self.client.chat.completions.create(

            model=self.models["vision"],

            messages=[
                {
                    "role": "system",
                    "content": """
You are Quantum Vision, the visual intelligence
system inside Quantum OS.

Analyze the supplied image carefully.

You can describe:
- Objects
- Animals
- Plants
- Vehicles
- Buildings
- Devices
- Text
- Scenes
- General visual information

Do not invent objects that are not visible.

If something is uncertain, say that you are
not certain.

Do not identify a real person by name from an image.
"""
                },

                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url":
                                "data:image/jpeg;base64,"
                                + image_base64
                            }
                        }
                    ]
                }
            ],

            temperature=0.2,
            max_tokens=1200
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

            language="en",

            response_format="json"
        )

        return response.text

    # ==========================================
    # CHANGE MODEL
    # ==========================================

    def set_model(self, capability, model):

        if capability not in self.models:
            raise ValueError(
                f"Unknown capability: {capability}"
            )

        self.models[capability] = model

    # ==========================================
    # SHOW MODELS
    # ==========================================

    def get_models(self):

        return self.models.copy()