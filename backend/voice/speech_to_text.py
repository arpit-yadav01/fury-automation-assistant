# voice/speech_to_text.py

import speech_recognition as sr


recognizer = sr.Recognizer()


def listen_once():

    with sr.Microphone() as source:

        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except sr.UnknownValueError:

        print("Could not understand")

    except sr.RequestError:

        print("Speech service error")

    return None