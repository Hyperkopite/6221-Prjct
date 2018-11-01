#!/usr/bin/env python3

#This module is used to find out is everything needed have been
#properly installed and ready to run.
#If not, run script automatically to install what missed.

"""
Check the availability of a user specified command line tool. And initialize the machine
"""

import subprocess
import re

def checkAvailability(commandline):
    """
    The main function of this module, for user to call in a more easier way.
    """

    s_lists = subprocess.getoutput(commandline)
    #return None if didn't find a match
    o_find = re.search(r'not found', s_lists)
    #extract the tool name from variable 'commandline'
    s_choose = commandline.split(" ")[0]

    if (o_find):
        #define a dictionary switcher that will return the proper function need to be executed
        switcher = {
                "tcpdump":getTcpdump
                #Add more here
        }

        func = switcher.get(s_choose)
        func()
    else:
        print("Tool " + s_choose + ": Check!")

def getTcpdump():
    """
    Get commandline tool tcpdump.
    """

    subprocess.run(["add-apt-repository", "universe"])
    subprocess.run(["add-apt-repository", "ppa:wireshark-dev/stable"])
    subprocess.run(["apt-get", "install", "wireshark"])



def main():
    checkAvailability("tcpdump --version")


if __name__ == '__main__':
    main()
