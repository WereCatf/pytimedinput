pytimedinput
============

Description
-----------

A tiny, simplistic little alternative to the standard Python input()-function allowing you to specify an optional timeout for the function.

pytimedinput should work on both Windows and Linux, though no exceedingly extensive testing has been done and there might be bugs.

Install
-------

.. code:: bash

    $ pip3 install pytimedinput

Usage
-----

timedInput()
............

*timedInput()* works similar to Python's default *input()* - function, asking user for a string of text, but *timedInput()* allows you to define an amount of time the user has to enter any text or how many consecutive seconds to wait for input, if the user goes idle.

.. code:: python

    def timedInput(prompt="", timeout=5, resetOnInput=True, maxLength=0, allowCharacters="", endCharacters="\x1b\n\r")

The function *timedInput()* from *pytimedinput* accepts the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds, use -1 to disable.*
 - **resetOnInput**, *bool*: Reset the timeout-timer any time user presses a key.
     *Defaults to True.*
 - **maxLength**, *int*: the maximum length of the string user is allowed to enter.
     *Defaults to 0, ie. unlimited.*
 - **allowCharacters**, *str*: Which characters the user is allowed to enter.
     *Defaults to "", ie. any character.*
 - **endCharacters**, *str*: On which characters to stop accepting input.
     *Defaults to "\\x1b\\n\\r", ie. ESC, newline and carriage-return. Cannot be empty.*

The function returns a tuple of:

 - *str*: a string containing whatever the user typed, regardless of whether the function timed out or not.
 - *bool*: whether the function timed out or not.

**Example:**

.. code:: python

    from pytimedinput import timedInput
    userText, timedOut = timedInput("Please, do enter something: ")
    if(timedOut):
        print("Timed out when waiting for input.")
        print(f"User-input so far: '{userText}'")
    else:
        print(f"User-input: '{userText}'")

timedKey()
..........
*timedKey()* waits for the user to press one of a set of predefined keys, with a timeout, while ignoring any keys not on the list.

.. code:: python

    def timedKey(prompt="", timeout=5, resetOnInput=True, allowCharacters="")

The function *timedKey()* from *pytimedinput* accepts the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds, use -1 to disable.*
 - **resetOnInput**, *bool*: Reset the timeout-timer any time user presses a key.
     *Defaults to True.*
 - **allowCharacters**, *str*: Which characters the user is allowed to enter.
     *Defaults to "", ie. any character.*

The function returns a tuple of:

 - *str*: a string containing the key the user pressed or an empty string.
 - *bool*: whether the function timed out or not.

**Example:**

.. code:: python

    from pytimedinput import timedKey
    userText, timedOut = timedKey("Please, press 'y' to accept or 'n' to decline: ", allowCharacters="yn")
    if(timedOut):
        print("Timed out when waiting for input. Pester the user later.")
    else:
        if(userText == "y"):
            print("User consented to selling their first-born child!")
        else:
            print("User unfortunately declined to sell their first-born child!")

**Tip: use timedKey() for the infamous "Press any key to continue."-prompt!**

.. code:: python

    from pytimedinput import timedKey
    timedKey("Press any key to continue.", timeout=-1)

timedInteger() and timedFloat()
...............................
*timedInteger()* and *timedFloat* work like *timedInput()*, except they only allow the user to enter numbers, and comma or period in case of *timedFloat*. Can be used to enter a negative number.

.. code:: python

    def timedInteger(prompt="", timeout=5, resetOnInput=True, allowNegative=True)

The function *timedInteger()* and *timedFloat()* from *pytimedinput* accept the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds, use -1 to disable.*
 - **resetOnInput**, *bool*: Reset the timeout-timer any time user presses a key.
     *Defaults to True.*
 - **allowNegative**, *bool*: Whether to allow the user to enter a negative value or not.

The function returns a tuple of:

 - *int/float* or *None*: an integer or float, depending on which function was called or None, if no number was entered.
 - *bool*: whether the function timed out or not.

**Example:**

.. code:: python

    from pytimedinput import *
    userNumber, timedOut = timedFloat("Enter a floating-point value: ")
    if(not timedOut):
        if(userNumber == None):
            print("We wanted a number, but got none.")
        else:
            print(f"We should do some fancy maths with {userNumber}!")


Exceptions
----------

All the functions require an interactive shell to function and will raise a Runtimerror-exception otherwise, which will need to be caught in any script that will be used both interactively and non-interactively.

License
-------

MIT