# agents/voice_agent.py

from agents.base_agent import BaseAgent

from voice.speech_to_text import listen_once
from voice.text_to_speech import speak


class VoiceAgent(BaseAgent):

    def __init__(self):
        super().__init__("VoiceAgent")

    # -------------------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("voice_input"):
            return True

        if task.get("voice_output"):
            return True

        return False

    # -------------------------

    def handle(self, task):

        # speech input

        if task.get("voice_input"):

            print("VoiceAgent → listen")

            text = listen_once()

            return text

        # speech output

        if task.get("voice_output"):

            text = task.get("text", "")

            speak(text)

            return