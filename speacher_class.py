import sys
import re
import speech_recognition
import os
import pyttsx3

recognizer = speech_recognition.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
engine.runAndWait()

class ChomeSpeacher():
    def __init__(self, appName, listenWord):
        self.appName = appName
        self.listenWord = listenWord

    def say(self, output):
        print(output)
        pyttsx3.speak(output)
    def output(self, output):
        print("output: " + output)
        pyttsx3.speak(output)

    def runCommand(self, newCommand):
        newCommand = newCommand.split(" ")
        if (newCommand[0].lower() != self.listenWord):
            return print("Wrong listener word.")
        if (len(newCommand) < 2):
            return self.output("Parameters are written wrong.")

        newCommand = {
            "paramCount": len(newCommand) - 1,
            "command": newCommand[1].lower(),
            "value": " ".join(newCommand[2:]),
            "valueList": newCommand[2:]
        }

        self.commandHandler(newCommand)

    def commandInput(self):
        newCommand = input()
        self.runCommand(newCommand)
        self.commandInput()

    def commandListener(self):
        answer = ""
        with speech_recognition.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            answer = recognizer.recognize_google(
                audio, key=None, language="en-US", show_all=False
            )
        except speech_recognition.UnknownValueError:
            print("UnknownValueError")
        print(answer)
        self.runCommand(answer)
        answer = None
        self.commandListener()

    def commandHandler(self, command):
        if (command["paramCount"] == 1):
            if (command["command"] == "exit"):
                sys.exit(1)

        elif (command["paramCount"] >= 2):

            if (command["command"] == "open"):
                currentCommand = "start %s" % command["value"]

                if (os.system(currentCommand) == 0):
                    return self.output(f"starting {command['valueList'][0]}")
                else:
                    return self.output(f"Can\'t open \"%s\"." % (command["value"]))


        self.output("Command does not exist.")