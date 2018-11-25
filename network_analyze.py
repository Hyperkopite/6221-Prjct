#!/usr/bin/env python3

#All the functions that related to network analyze
#Fuctions:
#  1.capture() ---- capture current network traffic and store them into a file.
#  2.analyzer() ---- analyze the network traffic file.

import subprocess
import re

""" Extract information from network traffic and analyze them """

def capture():
    subprocess.run(["bettercap", "-caplet", "commands.bettercap.cap"], True)


def main():
    print("Network Analyze!")
    capture()


if __name__ == '__main__':
    main()
