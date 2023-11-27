# asentry

## Monitor the JPL Sentry database for asteroid impact threats.

This program downloads a list of potential Earth-threatening asteroids
and displays an alert message if there are any new or increased threats
since the last time it ran.

If there is a sound file named "alert.mp3" in this directory, it will be
played when a warning message is displayed.

If any warning messages are displayed, the program waits for the user to
press Enter before exiting; otherwise it exits immediately. This is because
I have the program run at system startup and I need its window to stay open
so I can read the messages.

Copyright 2023 Len Popp - see LICENSE
