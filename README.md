# asentry

## Monitor the JPL Sentry database for asteroid impact threats

This program downloads a list of potential Earth-threatening asteroids
from NASA JPL's [Sentry](https://cneos.jpl.nasa.gov/sentry/) service
and displays an alert message if there are any new or increased threats
since the last time it ran.

If there is a sound file named "alert.mp3" in this directory, it will be
played when a warning message is displayed.

The program returns an exit code of 0 if there are no new threats, 1 if there
are new threats, or 2 if an error occurred.

Copyright 2023 Len Popp - see LICENSE
