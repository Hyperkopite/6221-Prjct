#!/usr/bin/env python3

#Every fuction that related to static status analyze should be putted here.
#Functions:
#  1.ipProtocol() ---- check which version of ip protocal are being used.
#  2.portServiceList()   ---- list all the ports that are being used and the services using them.
#  3.isTor()      ---- check whether we are under Tor or not.

""" Analyze static status and produce a report """
import subprocess
import re

def ipProtocol():
    """ check which ip protocol is in use """
    s_result = re.search(r'inet6.+', subprocess.getoutput('ifconfig')).group() #extract the line with inet6
    b_protocol = re.search(r'<link>', s_result) #<link> means ipv6 address is not in use
    if(b_protocol):
        print("Using ip protocol: ipv4")
    else:
        print("Using ip protocol: ipv6")


def portServiceList():
    """ use linux command 'lsof' to find out service-port pairs """
    l_result = subprocess.getoutput('lsof -i -n').split("\n")[1:] #the second line of output is the start of useful informations
    print("lprocess | lprotocol | lport | rprotocol")
    for s in l_result:
        o_result = re.search(r':(\d+)->.+:(\w+)', s) #find and extract the information of local port and remote protocol
        l_temp = s.split()
        if(o_result):
            print(l_temp[0] + "\t" + l_temp[-3] + "\t" + o_result.group(1) + "\t" + o_result.group(2))


def isTor():
    print("isTor?") #this part is left to be completed in the future


def report():
    print("--------------------")
    ipProtocol()
    print("--------------------")
    portServiceList()
    print("--------------------")
    isTor()
    print("--------------------")


def main():
    print("Status Analyze!")
    report()


if __name__ == '__main__':
    main()
