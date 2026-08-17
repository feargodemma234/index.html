import os
import io
import re
import wave
import tempfile

from groq import Groq


class QuantumAIManager:

    CHAT_MODEL = "openai/gpt-oss-20b"
    STT_MODEL = "whisper-large-v3-turbo"
    TTS_MODEL = "canopylabs/orpheus-v1-english"

    TTS_VOICE = "troy"

    def __init__(self):

        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is missing. "
                "Add it to Streamlit Secrets."
            )

        self.client = Groq(api_key=api_key)

    # --------------------------------
    # TEXT CHAT
    # --------------------------------

    def chat(self, messages):

        system_message = {
            "role": "system",
            "content": """
You are Quantum AI, the central intelligence of Quantum OS.

You are direct, helpful and conversational.

Do not reveal hidden reasoning or internal chain-of-thought.
Give the user the useful answer directly.

The Quantum Administration Empire contains:
AI, Robotics, Energy, Health, Space,
Sports, Manufacturing, Infrastructure,
Defense and Exploration.

You are not a vision system.
Do not claim to see images or cameras.
"""
        }

        clean_messages = [
            system_message
        ]

        for message in messages:

            role = message.get("role")

            if role not in ["user", "assistant"]:
                continue

            content = message.get("content", "")

            if not content:
                continue

            clean_messages.append(
                {
                    "role": role,
                    "content": content
                }
            )

        response = self.client.chat.completions.create(
            model=self.CHAT_MODEL,
            messages=clean_messages,
            temperature=0.7,
            max_completion_tokens=2048,
            reasoning_effort="low",
        )

        answer = response.choices[0].message.content

        if not answer:
            return "I couldn't generate a response."

        return answer.strip()

    # --------------------------------
    # SPEECH TO TEXT
    # --------------------------------

    def transcribe(self, audio_file):

        audio_bytes = audio_file.getvalue()

        if not audio_bytes:
            raise ValueError("No audio was recorded.")

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            temp.write(audio_bytes)
            temp_path = temp.name

        try:

            with open(temp_path, "rb") as file:

                result = self.client.audio.transcriptions.create(
                    file=file,
                    model=self.STT_MODEL,
                    language="en",
                    response_format="text",
                    temperature=0.0,
                )

            if isinstance(result, str):
                return result.strip()

            return result.text.strip()

        finally:

            try:
                os.remove(temp_path)
            except OSError:
                pass

    # --------------------------------
    # SPLIT TEXT FOR TTS
    # --------------------------------

    def split_for_tts(self, text, max_chars=180):

        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return []

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        chunks = []
        current = ""

        for sentence in sentences:

            if len(sentence) <= max_chars:

                if len(current) + len(sentence) + 1 <= max_chars:

                    current = (
                        f"{current} {sentence}"
                    ).strip()

                else:

                    if current:
                        chunks.append(current)

                    current = sentence

            else:

                words = sentence.split()

                for word in words:

                    if len(current) + len(word) + 1 <= max_chars:

                        current = (
                            f"{current} {word}"
                        ).strip()

                    else:

                        if current:
                            chunks.append(current)

                        current = word

        if current:
            chunks.append(current)

        return chunks

    # --------------------------------
    # GENERATE ONE WAV
    # --------------------------------

    def generate_wav(self, text):

        response = self.client.audio.speech.create(
            model=self.TTS_MODEL,
            voice=self.TTS_VOICE,
            input=text,
            response_format="wav",
        )

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            path = temp.name

        try:

            response.write_to_file(path)

            with open(path, "rb") as file:
                return file.read()

        finally:

            try:
                os.remove(path)
            except OSError:
                pass

    # --------------------------------
    # COMBINE WAV FILES
    # --------------------------------

    def combine_wavs(self, wav_files):

        if not wav_files:
            return None

        if len(wav_files) == 1:
            return wav_files[0]

        first = wave.open(
            io.BytesIO(wav_files[0]),
            "rb"
        )

        params = first.getparams()

        combined_frames = [
            first.readframes(first.getnframes())
        ]

        first.close()

        for data in wav_files[1:]:

            current = wave.open(
                io.BytesIO(data),
                "rb"
            )

            if (
                current.getnchannels()
                != params.nchannels
                or current.getsampwidth()
                != params.sampwidth
                or current.getframerate()
                != params.framerate
                or current.getcomptype()
                != params.comptype
            ):
                current.close()
                raise ValueError(
                    "The generated voice clips use incompatible WAV formats."
                )

            combined_frames.append(
                current.readframes(
                    current.getnframes()
                )
            )

            current.close()

        output = io.BytesIO()

        with wave.open(output, "wb") as writer:

            writer.setnchannels(
                params.nchannels
            )

            writer.setsampwidth(
                params.sampwidth
            )

            writer.setframerate(
                params.framerate
            )

            writer.setcomptype(
                params.comptype,
                params.compname
            )

            for frames in combined_frames:
                writer.writeframes(frames)

        return output.getvalue()

    # --------------------------------
    # TEXT TO SPEECH
    # --------------------------------

    def text_to_speech(self, text):

        chunks = self.split_for_tts(
            text,
            max_chars=180
        )

        if not chunks:
            return None

        wav_files = []

        for chunk in chunks:

            audio = self.generate_wav(
                chunk
            )

            if audio:
                wav_files.append(audio)

        return self.combine_wavs(
            wav_files
        )