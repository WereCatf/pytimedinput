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

.. code:: python

    def timedInput(prompt="", timeOut=5, forcedTimeout=False, endCharacters=['\x1b', '\n', '\r'])

The function timedInput() from pyTimedInput accepts the following parameters:
 - prompt, str: a string to show the user as a prompt when waiting for input.
     *Defaults to an empty string.*
 - timeout: how many seconds to wait before timing out.
     *Defaults to 5 seconds.*
 - forcedTimeout: whether to wait for 'timeout' many seconds consecutively or simply time out regardless of user-input.
     *Defaults to False, ie. consecutive.*
 - endCharacters[]: what characters to consider as end-of-input.
     *Defaults to new-line, carrier-feed and ESC-key.*

The function returns a string containing whatever user entered and a boolean whether the input timed out or not.

.. code:: python

    from pyTimedInput import timedInput
    userText, timedOut = timedInput("Please, do enter something: ")
    if(timedOut):
        print("Timed out when waiting for input.")
        print(f"User-input so far: '{userText}'")
    else:
        print(f"User-input: '{userText}'")

License
-------

MIT