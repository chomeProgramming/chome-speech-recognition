# import speech_recognition
# import re
# import speech_recognition as sr
# import asyncio
# import os
# import playsound
# from gtts import gTTS
# import requests
# import sys

# r = sr.Recognizer()


# def record_audio():
#     with sr.Microphone() as source:
#         audio = r.listen(source)
#         voice_data = ""
#         try:
#             voice_data = r.recognize_google(audio)
#         except sr.UnknownValueError:
#             print("Sorry, I did not get that")
#         except sr.RequestError:
#             print("Sorry, my speech service is down")
#         return voice_data


# def respond(voice_data):
#     if "stop" in voice_data:
#         sys.exit(0)
#     if "speak" in voice_data:
#         speak("yes")


# def speak(text):
#     print("ENGLISCH")
#     tts = gTTS(text=text, lang="en")
#     filename = "output.mp3"
#     tts.save(filename)
#     playsound.playsound(filename)
#     os.remove(filename)


# print("Hello, how can i help you?")


# def resolve():
#     return record_audio()


# async def loop():
#     temporary = resolve()
#     voice_data = await temporary
#     respond(voice_data)
#     asyncio.run(loop())

# asyncio.run(loop())

# https://pypi.org/project/SpeechRecognition/

import re
import speech_recognition


def loop():
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    words = recognizer.recognize_google(
        audio, key=None, language="en-US", show_all=False
    )

    matches = ""
    print(words)

    if matches:
        print(f"Hey, {matches[1]}.")
    else:
        print("Hey, you.")

    loop()

loop()
