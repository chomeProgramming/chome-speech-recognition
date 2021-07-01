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
        self.askType = "listen"

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
            return self.output("Parameters are wrong.")

        newCommand = {
            "paramCount": len(newCommand) - 1,
            "command": newCommand[1].lower(),
            "value": " ".join(newCommand[2:]),
            "valueList": newCommand[2:]
        }

        self.commandHandler(newCommand)

    def commandAsk(self):
        if self.askType == "write":
            self.commandInput()
        elif self.askType == "listen":
            self.commandListener()

    def commandInput(self):
        newCommand = input()
        self.runCommand(newCommand)
        self.commandAsk()

    def commandListener(self):
        answer = ""
        with speech_recognition.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                # audio = recognizer.listen(speech_recognition.Microphone())
                answer = recognizer.recognize_google(
                    audio, key=None, language="en-US", show_all=False
                )
            except speech_recognition.UnknownValueError:
                print("UnknownValueError")
        print(answer)
        self.runCommand(answer)
        answer = None
        self.commandAsk()

    def commandHandler(self, command):
        if command["paramCount"] == 1:
            if command["command"] == "exit":
                sys.exit(1)
            elif command["command"] == "help":
                self.output("writing help")
                return print(f'\nYou can start commands in this app with saying \"{self.listenWord}\" at beginning and say the command after that.\
                    \nIf you want to write something because you want to enter a link exactly, you can say: \"{self.listenWord} type enter\".\
                    \nIf you then want to be able to speak again, you say: \"{self.listenWord} type listen\".\
                    \nRead the introduction for more informations.\n\
                ')

        if command["paramCount"] >= 2:
            if command["command"] == "type":
                if command["value"] == "listen":
                    self.askType = "listen"
                    return self.output("changing to listen mode")
                elif command["value"] == "enter":
                    self.askType = "write"
                    return self.output("changing to write mode")

            if command["command"] == "open":
                currentCommand = "start %s" % command["value"]

                if os.system(currentCommand) == 0:
                    return self.output(f"starting {command['valueList'][0]}")
                else:
                    return self.output(f"Can\'t open \"%s\"." % (command["value"]))


        self.output("Command does not exist.")