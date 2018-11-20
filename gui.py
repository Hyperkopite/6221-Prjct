# -*- coding: utf-8 -*-
import time
import psutil
from tkinter import *
from tkinter import scrolledtext
import threading
import subprocess
import requests
import os


def get_ip_info():
    r = requests.get('http://api.ipstack.com/' + str(requests.get('http://httpbin.org/ip').json()['origin']) + '?access_key=f421a18339bb3370006ce3317acfb9a7')
    for strr in r.json():
        if strr != 'location':
            # print(strr + ': ' + str(r.json()[strr]))
            ip_info.insert(END, '\n' + strr + ': ' + str(r.json()[strr]) + '\n')
    ip_info.see(END)


def center_window_auto_full():
    # get the width and height of screen
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry('%dx%d' %(ws, hs))


def center_window(w, h):
    # get the width and height of screen
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate x,y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def io_get_bytes(sent=False, recv=False):
    internet = psutil.net_io_counters()  # get network info
    if internet is None:                 # if failed to get info
        return None
    io_sent = internet.bytes_sent        # bytes sent since launch
    io_recv = internet.bytes_recv        # bytes received since launch
    if sent and recv:
        return [io_sent, io_recv]
    elif sent:
        return io_sent
    elif recv:
        return io_recv
    else:
        return None                      # erroneous args,return none


def net_speed():
    interval = 1  # interval to get bytes info
    k = 1024  # 一 bytes for 1KB
    m = 1048576  # 一 bytes for 1 MB

    byteSent1 = io_get_bytes(sent=True)  # get bytes sent since launch
    byteRecv1 = io_get_bytes(recv=True)  # get bytes received since launch
    time.sleep(interval)  # interval
    byteSent2 = io_get_bytes(sent=True)  # get bytes sent since launch again
    byteRecv2 = io_get_bytes(recv=True)  # get bytes received since launch again
    sent = byteSent2 - byteSent1  # bytes sent in interval
    recv = byteRecv2 - byteRecv1  # bytes received in interval
    unit = 'B/s'  # Unit for B/S
    if sent > m or recv > m:  # Unit for MB/s
        sent = sent / m
        recv = recv / m
        unit = 'MB/s'
    if sent > k or recv > k:  # Unit for KB/s
        sent = sent / k
        recv = recv / k
        unit = 'KB/s'

    txt_status.set('Upload: %5d %s' % (int(sent), unit) + '   Download: %5d %s' % (int(recv), unit))  # Update statusBar
    status.pack(side=BOTTOM, fill=X)
    cap()
    global timer  # for recursively refreshing status bar and sniff data
    timer = threading.Timer(0, net_speed)
    timer.start()


def net_info_center():
    # central_info.delete(0.0, END)
    output = subprocess.Popen('ifconfig', stdout=subprocess.PIPE, shell=True, universal_newlines=True).communicate()
    ip_info.insert(END, output[0])
    output = subprocess.Popen('iwconfig', stdout=subprocess.PIPE, shell=True, universal_newlines=True).communicate()
    ip_info.insert(END, output[0])
    # global timer_net_info_center
    # timer_net_info_center = threading.Timer(1, net_info_center)
    # timer_net_info_center.start()


def cap():
    central_info.insert(END, bettercap.stdout.readline())
    central_info.see(END)


def quit():
    os.system('pkill bettercap')
    root.destroy()
# start from h


root = Tk()

center_window_auto_full()
root.title('Protector')

frame_btns = Frame(root)
frame_center = Frame(root)
frame_right = Frame(root)

ip_info = scrolledtext.ScrolledText(frame_right, width=int(root.winfo_screenwidth() / 10), height=int(root.winfo_screenheight() / 8), relief=GROOVE, wrap=WORD)
ip_info.pack()

central_info = scrolledtext.ScrolledText(frame_center, width=int(root.winfo_screenwidth() / 15), height=int (root.winfo_screenheight() / 6), relief=GROOVE, wrap=WORD)
central_info.pack()
net_info_center()
get_ip_info()

bettercap = subprocess.Popen('bettercap -X -L', stdout=subprocess.PIPE, shell=True, universal_newlines=True)

txt_status = StringVar()
status = Label(root, textvariable=txt_status, bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
net_speed()

btn_wifi_browse = Button(frame_btns, text='Show APs', width=int(root.winfo_screenwidth() / 120), height=2)
btn_wifi_browse.pack(side=LEFT)

btn_analyze = Button(frame_btns, text='Analyze', width=int(root.winfo_screenwidth() / 120), height=2)
btn_analyze.pack(side=LEFT)

btn_Fun3 = Button(frame_btns, text='Fun3', width=int(root.winfo_screenwidth() / 120), height=2)
btn_Fun3.pack(side=LEFT)

btn_Fun4 = Button(frame_btns, text='Fun4', width=int(root.winfo_screenwidth() / 120), height=2)
btn_Fun4.pack(side=LEFT)

btn_Fun5 = Button(frame_btns, text='Fun5', width=int(root.winfo_screenwidth() / 120), height=2)
btn_Fun5.pack(side=LEFT)

btn_quit = Button(frame_btns, text='Quit', width=int(root.winfo_screenwidth() / 120), height=2, command=quit)
btn_quit.pack(side=LEFT)

frame_btns.pack(side=TOP, fill=BOTH, padx=int(root.winfo_screenwidth() / 7), pady=int(root.winfo_screenwidth() / 25))
frame_center.pack(side=LEFT, padx=int(root.winfo_screenwidth() / 25), pady=int(root.winfo_screenwidth() / 30))
frame_right.pack(side=RIGHT, padx=int(root.winfo_screenwidth() / 20), pady=int(root.winfo_screenwidth() / 18))

mainloop()
