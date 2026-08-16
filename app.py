import re
import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        self.model = "qwen/qwen3.6-27b"

    def clean_response(self, text):
        """
        Remove thinking/reasoning blocks if the model
        accidentally returns them.
        """

        # Remove <think>...</think>
        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Remove an unfinished <think> block
        text = re.sub(
            r"<think>.*$",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Remove other common reasoning markers
        text = re.sub(
            r"^(Here'?s a thinking process:|"
            r"Let me think:|"
            r"Thinking:)\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        return text.strip()

    def text(self, prompt, history=None):

        messages = [
            {
                "role": "system",
                "content": """
You are Quantum AI, the central AI of Quantum OS.

You are part of The Quantum Administration Empire.

Your job is to answer the user's request directly.

IMPORTANT RESPONSE RULES:

1. Do NOT reveal your reasoning process.
2. Do NOT output <think> tags.
3. Do NOT describe your internal thinking.
4. Do NOT say "Here's my thinking process".
5. Do NOT provide step-by-step hidden reasoning.
6. Give the answer directly.
7. Keep simple questions concise.
8. Give more detail only when it is useful.
9. If the user asks for code, provide the code directly.
10. If you don't know something, say so clearly.

Empire divisions:

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

You can help with programming,
science, engineering, business,
technology and development of Quantum OS.

Always communicate naturally and directly.
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
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=2000
        )

        answer = response.choices[0].message.content

        return self.clean_response(answer)

    def get_model(self):
        return self.model