import streamlit as st
from groq import Groq


class QuantumAIManager:

    def __init__(self):
        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        # TEXT ONLY
        # NO VISION
        self.model = "llama-3.3-70b-versatile"

        self.system_prompt = """
You are Quantum AI, the central intelligence of Quantum OS.

You are part of The Quantum Administration Empire.

The Empire has these divisions:

1. AI
2. Robotics
3. Energy
4. Health
5. Space
6. Sports
7. Manufacturing
8. Infrastructure
9. Defense
10. Exploration

Your personality:
- Direct
- Intelligent
- Helpful
- Clear
- Conversational

Answer the user's question directly.

IMPORTANT:
Do not reveal hidden reasoning.
Do not output internal analysis.
Do not output <think> tags.
Do not describe your chain of thought.
Give only the final answer.
"""

    def chat(self, user_message, history=None):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        # Add previous conversation
        if history:
            messages.extend(history)

        # Add current message
        messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )

        answer = response.choices[0].message.content or ""

        # Safety cleanup in case the model returns thinking tags
        if "<think>" in answer:
            answer = answer.split("<think>", 1)[1]

            if "</think>" in answer:
                answer = answer.split("</think>", 1)[1]

        return answer.strip()