import sys
from typing import Tuple
if(sys.platform == "win32"):
    import msvcrt
else:
    import select
    import tty
    import termios
import time


# '\x1b' == ESC
def timedInput(prompt: str = "", timeOut: int = 5, forcedTimeout: bool = False, endCharacters: list = ['\x1b', '\n', '\r']) -> Tuple[str, bool]:
    if(not sys.__stdin__.isatty()):
        raise RuntimeError(
            "timedInput() requires an interactive shell, cannot continue.")
    userInput = ""
    timeStart = time.time()
    timedOut = False
    if(len(prompt) > 0):
        print(prompt, end='', flush=True)

    if(sys.platform == "win32"):
        while(True):
            if((time.time() - timeStart) >= timeOut):
                timedOut = True
                break
            if(msvcrt.kbhit()):
                inputCharacter = msvcrt.getwche()
                if(inputCharacter in endCharacters):
                    break
                userInput = userInput + inputCharacter
                if(not forcedTimeout):
                    timeStart = time.time()
        print("")
        return userInput, timedOut
    else:
        def checkStdin():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while True:
                if((time.time() - timeStart) >= timeOut):
                    timedOut = True
                    break
                if(checkStdin()):
                    inputCharacter = sys.stdin.read(1)
                    if(inputCharacter in endCharacters):
                        break
                    userInput = userInput + inputCharacter
                    print(inputCharacter, end='', flush=True)
                    if(not forcedTimeout):
                        timeStart = time.time()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            print("")
            return userInput, timedOut


def timedKey(prompt: str = "", timeOut: int = 5, forcedTimeout: bool = False, endCharacters: list = ['n', 'y']) -> Tuple[str, bool]:
    if(not sys.__stdin__.isatty()):
        raise RuntimeError(
            "timedKey() requires an interactive shell, cannot continue.")
    userInput = ""
    timeStart = time.time()
    timedOut = False
    if(len(prompt) > 0):
        print(prompt, end='', flush=True)

    if(sys.platform == "win32"):
        while(True):
            if((time.time() - timeStart) >= timeOut):
                timedOut = True
                break
            if(msvcrt.kbhit()):
                inputCharacter = msvcrt.getwche()
                if(inputCharacter in endCharacters):
                    userInput = inputCharacter
                    break
                print("\b \b", flush=True, end='')
                if(not forcedTimeout):
                    timeStart = time.time()
        print("")
        return userInput, timedOut
    else:
        def checkStdin():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while True:
                if((time.time() - timeStart) >= timeOut):
                    timedOut = True
                    break
                if(checkStdin()):
                    inputCharacter = sys.stdin.read(1)
                    if(inputCharacter in endCharacters):
                        userInput = inputCharacter
                        print(inputCharacter, end='', flush=True)
                        break
                    if(not forcedTimeout):
                        timeStart = time.time()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            print("")
            return userInput, timedOut
