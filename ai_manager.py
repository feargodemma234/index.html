import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        # TEXT ONLY — NO VISION
        self.text_model = "llama-3.3-70b-versatile"

        # VOICE INPUT
        self.voice_model = "whisper-large-v3-turbo"

        # VOICE OUTPUT
        self.tts_model = "canopylabs/orpheus-v1-english"
        self.voice = "troy"

        self.system_prompt = """
You are Quantum AI, the central intelligence of Quantum OS.

You are part of The Quantum Administration Empire.

The Empire includes:
AI, Robotics, Energy, Health, Space, Sports,
Manufacturing, Infrastructure, Defense, Exploration.

Be direct, helpful, accurate, and conversational.

Give only the final answer.
Do not reveal internal reasoning.
Do not output <think> tags.
Do not describe hidden reasoning.
"""

    def chat(self, prompt, history=None):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
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

        answer = response.choices[0].message.content or ""

        if "<think>" in answer:
            answer = answer.split("<think>", 1)[1]

            if "</think>" in answer:
                answer = answer.split("</think>", 1)[1]

        return answer.strip()

    def transcribe(self, audio_file):

        result = self.client.audio.transcriptions.create(
            file=audio_file,
            model=self.voice_model,
            language="en",
            response_format="json"
        )

        return result.text.strip()

    def speak(self, text):

        # Groq's Orpheus endpoint currently limits input
        # to 200 characters, so keep the spoken response short.
        text = text[:200]

        response = self.client.audio.speech.create(
            model=self.tts_model,
            voice=self.voice,
            input=text,
            response_format="wav"
        )

        return response.read()