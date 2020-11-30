pyTimedInput
============

Description
-----------

A tiny, simplistic little alternative to the standard Python input()-function allowing you to specify a timeout for the function.

pyTimedInput should work on both Windows and Linux, though no exceedingly extensive testing has been done and there might be bugs.

Install
-------

.. code:: bash

    $ pip3 install pyTimedInput

Usage
-----

*timedInput()* works similar to Python's default *input()* - function, asking user for a string of text, but *timedInput()* allows you to also define an amount of time the user has to enter any text or how many consecutive seconds to wait for input, if the user goes idle.

.. code:: python

    def timedInput(prompt="", timeOut=5, forcedTimeout=False, endCharacters=['\x1b', '\n', '\r'])

The function *timedInput()* from *pyTimedInput* accepts the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds.*
 - **forcedTimeout**, *bool*: whether to wait for 'timeout' many consecutive seconds of idle time or simply time out regardless of user-input.
     *Defaults to False, ie. consecutive.*
 - **endCharacters** [], *list*: what characters to consider as end-of-input.
     *Defaults to new-line, carrier-feed and ESC-key.*

The function returns a tuple of:

 - *str*: a string containing whatever the user typed, regardless of whether the function timed out or not.
 - *bool*: whether the function timed out or not.

.. code:: python

    from pyTimedInput import timedInput
    userText, timedOut = timedInput("Please, do enter something: ")
    if(timedOut):
        print("Timed out when waiting for input.")
        print(f"User-input so far: '{userText}'")
    else:
        print(f"User-input: '{userText}'")


*timedKey()* waits for the user to press one of a set of predefined keys, with a timeout, while ignoring any keys not on the list.

.. code:: python

    def timedKey(prompt="", timeOut=5, forcedTimeout=False, endCharacters=['y', 'n'])

The function *timedKey()* from *pyTimedInput* accepts the following parameters:

 - **prompt**, *str*: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - **timeout**, *int*: how many seconds to wait before timing out.
     *Defaults to 5 seconds.*
 - **forcedTimeout**, *bool*: whether to wait for 'timeout' many consecutive seconds of idle time or simply time out regardless of user-input.
     *Defaults to False, ie. consecutive.*
 - **endCharacters** [], *list*: what characters to accept.
     *Defaults to 'y' and 'n'.*

The function returns a tuple of:

 - *str*: a string containing the key user pressed, if on the endCharacters - list, or an empty string.
 - *bool*: whether the function timed out or not.

.. code:: python

    from pyTimedInput import timedKey
    userText, timedOut = timedKey("Please, press 'y' to accept or 'n' to decline: ", endCharacters=['y', 'n'])
    if(timedOut):
        print("Timed out when waiting for input. Pester the user later.")
    else:
        if(userText == "y"):
            print("User consented to selling their first-born child!")
        else:
            print("User unfortunately declined to sell their first-born child!")

Exceptions
----------

Both *timedInput()* and *timedKey()* require an interactive shell to function and will raise a Runtimerror - exception otherwise, which will need to be caught in any script that will be used both interactively and non-interactively.

License
-------

MIT