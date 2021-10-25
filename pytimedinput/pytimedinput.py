import sys
import time
from typing import Tuple, Union
if(sys.platform == "win32"):
    import msvcrt
    import ctypes
    from ctypes import wintypes
else:
    import select
    import tty
    import termios


def timedInput(prompt: str = "", timeout: int = 5, resetOnInput: bool = True, maxLength: int = 0, allowCharacters: str = "", endCharacters: str = "\x1b\n\r") -> Tuple[str, bool]:
    """Ask the user for text input with an optional timeout and limit on allowed characters.

    Args:
        prompt (str, optional): The prompt to be displayed to the user. Defaults to "".
        timeout (int, optional): How many seconds to wait for input. Defaults to 5, use -1 to wait forever.
        resetOnInput (bool, optional): Reset the timeout-timer any time user presses a key. Defaults to True.
        maxLength (int, optional): Maximum length of input user is to be allowed to type. Defaults to 0, use 0 to disable. 
        allowCharacters (str, optional): Which characters the user is allowed to enter. Defaults to "", ie. any character.
        endCharacters (str, optional): On which characters to stop accepting input. Defaults to "\\x1b\\n\\r", ie. ESC and Enter. Cannot be empty.

    Returns:
        Tuple[str, bool]: The characters input by the user and whether the input timed out or not.
    """
    if(maxLength < 0):
        return "", False
    if(len(endCharacters) == 0):
        return "", False
    return __timedInput(prompt, timeout, resetOnInput, maxLength, allowCharacters, endCharacters)


def timedKey(prompt: str = "", timeout: int = 5, resetOnInput: bool = True, allowCharacters: str = "") -> Tuple[str, bool]:
    """Ask the user to press a single key out of an optional list of allowed ones.

    Args:
        prompt (str, optional): The prompt to be displayed to the user. Defaults to "".
        timeout (int, optional): How many seconds to wait for input. Defaults to 5, use -1 to wait forever.
        resetOnInput (bool, optional): Reset the timeout-timer any time user presses a key. Defaults to True.
        allowCharacters (str, optional): Which characters the user is allowed to enter. Defaults to "", ie. any character.

    Returns:
        Tuple[str, bool]: Which key the user pressed and whether the input timed out or not.
    """
    return __timedInput(prompt, timeout, resetOnInput, maxLength=1, allowCharacters=allowCharacters, endCharacters="", inputType="single")


def timedInteger(prompt: str = "", timeout: int = 5, resetOnInput: bool = True, allowNegative: bool = True) -> Tuple[Union[int, None], bool]:
    """Ask the user to enter an integer value.

    Args:
        prompt (str, optional): The prompt to be displayed to the user. Defaults to "".
        timeout (int, optional): How many seconds to wait for input. Defaults to 5, use -1 to wait forever.
        resetOnInput (bool, optional): Reset the timeout-timer any time user presses a key. Defaults to True.
        allowNegative (bool, optional): Whether to allow the user to enter a negative value or not.

    Returns:
        Tuple[Union[int, None], bool]: The value entered by the user and whether the input timed out or not.
    """
    userInput, timedOut = __timedInput(
        prompt, timeout, resetOnInput, allowCharacters="-" if(allowNegative) else "", inputType="integer")
    try:
        return int(userInput), timedOut
    except:
        return None, timedOut


def timedFloat(prompt: str = "", timeout: int = 5, resetOnInput: bool = True, allowNegative: bool = True) -> Tuple[Union[float, None], bool]:
    """Ask the user to enter a floating-point value.

    Args:
        prompt (str, optional): The prompt to be displayed to the user. Defaults to "".
        timeout (int, optional): How many seconds to wait for input. Defaults to 5, use -1 to wait forever.
        resetOnInput (bool, optional): Reset the timeout-timer any time user presses a key. Defaults to True.
        allowNegative (bool, optional): Whether to allow the user to enter a negative value or not.

    Returns:
        Tuple[Union[float, None], bool]: The value entered by the user and whether the input timed out or not.
    """
    userInput, timedOut = __timedInput(
        prompt, timeout, resetOnInput, allowCharacters="-" if(allowNegative) else "", inputType="float")
    try:
        return float(userInput), timedOut
    except:
        return None, timedOut


def __timedInput(prompt: str = "", timeout: int = 5, resetOnInput: bool = True, maxLength: int = 0, allowCharacters: str = "", endCharacters: str = "\x1b\n\r", inputType: str = "text") -> Tuple[str, bool]:
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

    if(not sys.__stdin__.isatty()):
        raise RuntimeError(
            "timedInput() requires an interactive shell, cannot continue.")
    else:
        __savedConsoleSettings = __getStdoutSettings()
        __enableStdoutAnsiEscape()

        numbers = "01234567890"
        if(inputType == "integer"):
            allowCharacters += numbers
        if(inputType == "float"):
            allowCharacters += numbers + ".,"

        userInput = ""
        timeStart = time.time()
        timedOut = False
        if(len(prompt) > 0):
            print(prompt, end='', flush=True)

        while(True):
            if(timeout > -1 and (time.time() - timeStart) >= timeout):
                timedOut = True
                break
            if(checkStdin()):
                inputCharacter = readStdin()
                if(inputCharacter in endCharacters):
                    break
                if(inputCharacter != '\b' and inputCharacter != '\x7f'):
                    if(len(allowCharacters) and not inputCharacter in allowCharacters):
                        inputCharacter = ""
                    if(inputCharacter == "-" and inputType in ["integer", "float"]):
                        if(len(userInput) > 0):
                            inputCharacter = ""
                    if(maxLength > 0 and len(userInput) >= maxLength):
                        inputCharacter = ""
                    if(inputType == "float"):
                        if(inputCharacter == ","):
                            inputCharacter = "."
                        if(inputCharacter == "." and inputCharacter in userInput):
                            inputCharacter = ""
                    userInput = userInput + inputCharacter
                    print(inputCharacter, end='', flush=True)
                    if(maxLength == 1 and len(userInput) == 1 and inputType == "single"):
                        break
                else:
                    if(len(userInput)):
                        userInput = userInput[0:len(userInput) - 1]
                        print("\x1b[1D\x1b[0K", end='', flush=True)
                if(resetOnInput and timeout > -1):
                    timeStart = time.time()
        print("")
        __setStdoutSettings(__savedConsoleSettings)
        return userInput, timedOut


def __getStdoutSettings():
    if(sys.platform == "win32"):
        __savedConsoleSettings = wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        # The Windows standard handle -11 is stdout
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-11), ctypes.byref(__savedConsoleSettings))
    else:
        __savedConsoleSettings = termios.tcgetattr(sys.stdin)
    return __savedConsoleSettings


def __setStdoutSettings(__savedConsoleSettings):
    if(sys.platform == "win32"):
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(
            kernel32.GetStdHandle(-11), __savedConsoleSettings)
    else:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, __savedConsoleSettings)


def __enableStdoutAnsiEscape():
    if(sys.platform == "win32"):
        kernel32 = ctypes.windll.kernel32
        # Enable ANSI escape sequence parsing
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        # Should be enabled by default under Linux (and OSX?), just set cbreak-mode
        tty.setcbreak(sys.stdin.fileno(), termios.TCSADRAIN)
