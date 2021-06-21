import sys
import re
import webbrowser

webbrowser.register("chrome",
    None,
    webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe")
)

def runCommand(newCommand):
    newCommand = newCommand.split(" ")
    if (newCommand[0] != "run" or len(newCommand) < 3):
        return print("Command is written wrong.")
    newCommand = {
        "command": newCommand[1],
        "value": newCommand[2]
    }

    if (newCommand["command"] == "open"):
        try:
            webbrowser.get("chrome").open(newCommand["value"])
        except:
            print(f"Error happend at: opening \"%s\"" % (newCommand["value"]))
    else:
        print("Command does not exist or you wrote it wrong.")

def commandInput():
    newCommand = input()
    runCommand(newCommand)
    commandInput()

commandInput()