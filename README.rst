pytimedinput
============

Description
-----------

A tiny, simplistic little alternative to the standard Python input()-function allowing you to specify a timeout for the function.

pytimedinput should work on both Windows and Linux, though no exceedingly extensive testing has been done and there might be bugs.

Install
-------

.. code:: bash

    $ pip3 install pytimedinput

Usage
-----

timedInput()
............

*timedInput()* works similar to Python's default *input()* - function, asking user for a string of text, but *timedInput()* allows you to define an amount of time the user has to enter any text or how many consecutive seconds to wait for input, if the user goes idle. Pressing ENTER, carriage-return or ESC will end input and return from the function.

.. code:: python

    def timedInput(prompt="", timeOut=5, forcedTimeout=False, maxLength=0)

The function *timedInput()* from *pytimedinput* accepts the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds.*
 - **forcedTimeout**, *bool*: whether to wait for 'timeout' many consecutive seconds of idle time or simply time out regardless of user-input.
     *Defaults to False, ie. consecutive.*
 - **maxLength** [], *int*: the maximum length of the string user is allowed to enter.
     *Defaults to 0, ie. unlimited.*

The function returns a tuple of:

 - *str*: a string containing whatever the user typed, regardless of whether the function timed out or not.
 - *bool*: whether the function timed out or not.

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

    def timedKey(prompt="", timeOut=5, forcedTimeout=False, allowCharacters=['y', 'n'])

The function *timedKey()* from *pytimedinput* accepts the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds.*
 - **forcedTimeout**, *bool*: whether to wait for 'timeout' many consecutive seconds of idle time or simply time out regardless of user-input.
     *Defaults to False, ie. consecutive.*
 - **allowCharacters** [], *list*: list of valid characters for the user to use.
     *Defaults to 'y' and 'n'.*

The function returns a tuple of:

 - *str*: a string containing the key user pressed, if on the endCharacters - list, or an empty string.
 - *bool*: whether the function timed out or not.

.. code:: python

    from pytimedinput import timedKey
    userText, timedOut = timedKey("Please, press 'y' to accept or 'n' to decline: ", endCharacters=['y', 'n'])
    if(timedOut):
        print("Timed out when waiting for input. Pester the user later.")
    else:
        if(userText == "y"):
            print("User consented to selling their first-born child!")
        else:
            print("User unfortunately declined to sell their first-born child!")

timedInteger() and timedFloat()
...............................
*timedInteger()* and *timedFloat* work like *timedInput()*, except only allows the user to enter numbers, and comma or period in case of *timedFloat*.

.. code:: python

    def timedInteger(prompt="", timeOut=5, forcedTimeout=False, maxLength=0)

The function *timedInteger()* and *timedFloat()* from *pytimedinput* accept the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds.*
 - **forcedTimeout**, *bool*: whether to wait for 'timeout' many consecutive seconds of idle time or simply time out regardless of user-input.
     *Defaults to False, ie. consecutive.*
 - **maxLength** [], *int*: the maximum length of numbers the user is allowed to enter. The decimal-separator does not count.
     *Defaults to 0, ie. unlimited.*

The function returns a tuple of:

 - *int/float* or *None*: an integer or float, depending on which function was called or None, if no number was entered.
 - *bool*: whether the function timed out or not.

.. code:: python

    from pytimedinput import *
    userText, timedOut = timedInput("Please, do enter something: ")
    if(timedOut):
        print("Timed out when waiting for input.")
        print(f"User-input so far: '{userText}'")
    else:
        print(f"User-input: '{userText}'")
    userNumber, timedOut = timedFloat("Enter a number: ", maxLength = 5)
    if(not timedOut):
        if(userNumber == None):
            print("We wanted a number, but got none.")
        else:
            print(f"We should do some fancy maths with {userNumber}!")


Exceptions
----------

Both *timedInput()* and *timedKey()* require an interactive shell to function and will raise a Runtimerror - exception otherwise, which will need to be caught in any script that will be used both interactively and non-interactively.

License
-------

MIT