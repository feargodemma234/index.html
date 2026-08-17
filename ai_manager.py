import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        self.text_model = "# OLD
model="llama-3.1-70b-versatile"
        self.stt_model = "whisper-large-v3-turbo"
        self.tts_model = "canopylabs/orpheus-v1-english"
        self.voice = "troy"

    def chat(self, text, history=None):

        messages = [
            {
                "role": "system",
                "content": """
You are Quantum AI, the central intelligence
of Quantum OS and The Quantum Administration Empire.

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

Be direct, helpful, natural and conversational.

Give only the final answer.
Never output <think> tags.
Never reveal hidden reasoning.
"""
            }
        ]

        if history:
            messages.extend(history)

        messages.append({
            "role": "user",
            "content": text
        })

        response = self.client.chat.completions.create(
            model=self.text_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        answer = response.choices[0].message.content or ""

        if "<think>" in answer:
            answer = answer.split("<think>", 1)[1]

            if "</think>" in answer:
                answer = answer.split("</think>", 1)[1]

        return answer.strip()

    def transcribe(self, audio_bytes):

        result = self.client.audio.transcriptions.create(
            file=(
                "voice.wav",
                audio_bytes,
                "audio/wav"
            ),
            model=self.stt_model,
            response_format="json"
        )

        return result.text.strip()

    def speak(self, text):

        # Keep the spoken response short enough
        # for the TTS endpoint.
        text = text[:200]

        response = self.client.audio.speech.create(
            model=self.tts_model,
            voice=self.voice,
            input=text,
            response_format="wav"
        )

        return response.read()