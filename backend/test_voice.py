from voice.speech_to_text import listen_once


print("Voice test started. Say 'exit' to stop.")


while True:

    text = listen_once()

    if text:
        print("TEXT:", text)

    if text == "exit":
        break