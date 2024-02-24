#!/bin/sh
py -m pip install requests
# this doens't work:
# py -m pip install playsound
py -m pip install playsound@git+https://github.com/taconi/playsound
