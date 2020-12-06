import sys
from typing import Tuple, Union
if(sys.platform == "win32"):
    import msvcrt
    import colorama
    colorama.init(wrap=False)
    outStream = colorama.AnsiToWin32(sys.stdout).stream
else:
    import select
    import tty
    import termios
    outStream = sys.stdout
import time


# '\x1b' == ESC
def timedInput(prompt: str = "", timeOut: int = 5, forcedTimeout: bool = False, maxLength: int = 0) -> Tuple[str, bool]:
    return __timedInput(prompt, timeOut, forcedTimeout, maxLength, allowCharacters=[], endCharacters=['\x1b', '\n', '\r'])


def timedKey(prompt: str = "", timeOut: int = 5, forcedTimeout: bool = False, allowCharacters: list = ['n', 'y']) -> Tuple[str, bool]:
    return __timedInput(prompt, timeOut, forcedTimeout, maxLength=1, allowCharacters=allowCharacters, endCharacters=[], inputType="single")


def timedInteger(prompt: str = "", timeOut: int = 5, forcedTimeout: bool = False, maxLength: int = 0) -> Tuple[Union[int, None], bool]:
    userInput, timedOut = __timedInput(
        prompt, timeOut, forcedTimeout, maxLength, inputType="integer")
    try:
        return int(userInput), timedOut
    except:
        return None, timedOut


def timedFloat(prompt: str = "", timeOut: int = 5, forcedTimeout: bool = False, maxLength: int = 0) -> Tuple[Union[float, None], bool]:
    userInput, timedOut = __timedInput(
        prompt, timeOut, forcedTimeout, maxLength, inputType="float")
    try:
        return float(userInput), timedOut
    except:
        return None, timedOut


def __timedInput(prompt: str = "", timeOut: int = 5, forcedTimeout: bool = False, maxLength: int = 0, allowCharacters: list = [], endCharacters: list = ['\x1b', '\n', '\r'], inputType: str = "text") -> Tuple[str, bool]:
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if(inputType == "integer"):
        allowCharacters = numbers
    if(inputType == "float"):
        allowCharacters = numbers
        allowCharacters.append(".")
        allowCharacters.append(",")

    if(not sys.__stdin__.isatty()):
        raise RuntimeError(
            "timedInput() requires an interactive shell, cannot continue.")

    def checkStdin():
        if(sys.platform == "win32"):
            return msvcrt.kbhit()
        else:
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def readStdin():
        if(sys.platform == "win32"):
            return msvcrt.getwch()
        else:
            return sys.stdin.read(1)

    userInput = ""
    timeStart = time.time()
    timedOut = False
    periods = 0
    if(len(prompt) > 0):
        print(prompt, end='', flush=True, file=outStream)

    if(sys.platform != "win32"):
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    while(True):
        if((time.time() - timeStart) >= timeOut):
            timedOut = True
            break
        if(checkStdin()):
            inputCharacter = readStdin()
            if(inputCharacter in endCharacters):
                break
            if(inputCharacter != '\b' and inputCharacter != '\x7f'):
                if(len(allowCharacters) and not inputCharacter in allowCharacters):
                    inputCharacter = ""
                if(maxLength > 0):
                    if(inputType != "float" and len(userInput) >= maxLength):
                        inputCharacter = ""
                    elif((len(userInput) - periods) >= maxLength):
                        inputCharacter = ""
                if(inputType == "float"):
                    if(inputCharacter == ","):
                        inputCharacter = "."
                    if(inputCharacter == "."):
                        if(periods):
                            inputCharacter = ""
                        else:
                            periods = 1
                userInput = userInput + inputCharacter
                print(inputCharacter, end='', flush=True)
                if(maxLength == 1 and len(userInput) == 1 and inputType == "single"):
                    break
            else:
                if(len(userInput)):
                    removeCharacter = userInput[len(
                        userInput) - 1:len(userInput)]
                    if(removeCharacter == "."):
                        periods = 0
                    userInput = userInput[0:len(userInput) - 1]
                    print("\u001b[1D \u001b[1D", end='',
                          flush=True, file=outStream)
            if(not forcedTimeout):
                timeStart = time.time()
    print("")
    if(sys.platform != "win32"):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return userInput, timedOut
