import streamlit as st
from groq import Groq
import base64


class QuantumAIManager:

    def __init__(self):

        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        self.models = {
            "text": "llama-3.3-70b-versatile",
            "vision": "qwen/qwen3.6-27b"
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

Help the user with:
AI, software, robotics, energy, health,
space, sports, manufacturing,
infrastructure, defense, exploration,
science and business.

Be clear, useful and technically accurate.

Do not claim that hypothetical projects
already exist.
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

    # ==========================================
    # VISION
    # ==========================================

    def vision(self, question, image_bytes):

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

Analyze the supplied image carefully.

Identify visible:
- Objects
- Animals
- Plants
- Vehicles
- Buildings
- Devices
- Machines
- Text
- Scenes
- General visual information

Describe what is actually visible.

Do not invent objects.

If you are uncertain about something,
clearly say that you are uncertain.

Do not identify people by name.
"""
                },

                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
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
            max_completion_tokens=1200
        )

        return response.choices[0].message.content

    # ==========================================
    # MODEL INFORMATION
    # ==========================================

    def get_models(self):

        return self.models.copy()