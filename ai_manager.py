import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):

        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        # Change these model names later
        # without changing the rest of Quantum OS.

        self.models = {
            "text": "llama-3.3-70b-versatile",
            "vision": "meta-llama/llama-4-scout-17b-16e-instruct",
            "speech_to_text": "whisper-large-v3-turbo"
        }


    # ==================================
    # TEXT AI
    # ==================================

    def text(self, prompt, history=None):

        messages = [
            {
                "role": "system",
                "content": """
You are Quantum AI.

You are the central intelligence
of Quantum OS and part of
The Quantum Administration Empire.

Help with AI, software, robotics,
energy, health, space, sports,
manufacturing, infrastructure,
defense and exploration.

Be helpful, accurate and clear.
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
            max_tokens=2000
        )

        return response.choices[0].message.content


    # ==================================
    # VISION
    # ==================================

    def vision(self, prompt, image_bytes):

        import base64

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        response = self.client.chat.completions.create(

            model=self.models["vision"],

            messages=[
                {
                    "role": "system",
                    "content": """
You are Quantum Vision.

Analyze images carefully.

Identify visible objects,
animals, environments, text,
equipment and other visual information.

Do not invent things that aren't
visible in the image.

If uncertain, say so.
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
                                f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],

            temperature=0.2,

            max_tokens=1000
        )

        return response.choices[0].message.content


    # ==================================
    # SPEECH TO TEXT
    # ==================================

    def transcribe(self, audio_bytes):

        response = self.client.audio.transcriptions.create(

            file=(
                "quantum_voice.wav",
                audio_bytes,
                "audio/wav"
            ),

            model=self.models["speech_to_text"]
        )

        return response.text


    # ==================================
    # CHANGE MODEL
    # ==================================

    def set_model(self, capability, model):

        if capability not in self.models:

            raise ValueError(
                f"Unknown capability: {capability}"
            )

        self.models[capability] = model


    # ==================================
    # GET CURRENT MODELS
    # ==================================

    def get_models(self):

        return self.models