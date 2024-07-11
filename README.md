# asentry

## Software to warn of potential asteroid impacts

This program downloads a list of potential Earth-threatening asteroids
from NASA JPL's [Sentry](https://cneos.jpl.nasa.gov/sentry/) service
and displays an alert message if there are any new or increased threats
since the last time it ran.

<i>(For a stand-alone device to do the same thing,
[click here](https://github.com/Len42/asentry-gadget?tab=readme-ov-file#asentry-gadget).)</i>

If there is a sound file named "alert.mp3" in this directory, it will be
played when a warning message is displayed.

The program returns an exit code of 0 if there are no new threats, 1 if there
are new threats, or 2 if an error occurred.

Sample output:

    $ py asentry.py
    WARNING: New threat: (2024 BY15)
    Impact date 2071-2124, Palermo = -3.30, Torino = 0
    Details: https://cneos.jpl.nasa.gov/sentry/details.html#?des=2024 BY15

PyPI modules required:
- requests
- playsound3

Copyright 2023 Len Popp - see LICENSE
