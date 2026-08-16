import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        # Text AI only — NO VISION
        self.text_model = "qwen/qwen3.6-27b"

    def text(self, prompt, history=None):

        messages = [
            {
                "role": "system",
                "content": """
You are Quantum AI, the central intelligence of Quantum OS.

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

Be direct, useful, accurate, and conversational.

Give the user ONLY the final answer.
Do not output internal reasoning.
Do not output analysis.
Do not output <think> tags.
Do not describe your hidden reasoning.
"""
            }
        ]

        if history:
            for message in history:
                messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })

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