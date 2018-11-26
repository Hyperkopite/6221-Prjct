# -*- coding: utf-8 -*-
import time
import psutil
from tkinter import *
from tkinter import scrolledtext
from tkinter import font
import tkinter as tk
import threading
import subprocess
import requests
import os


class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)

    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


def get_ip_info():
    r = requests.get('http://api.ipstack.com/' + str(requests.get('http://httpbin.org/ip').json()['origin']) + '?access_key=f421a18339bb3370006ce3317acfb9a7')
    geo_info = ''
    for strr in r.json():
        if strr == 'ip' or strr == 'city' or strr == 'country_name' or strr == 'type' or strr == 'region_name' or strr == 'latitude' or strr == 'longitude':
            # print(strr + ': ' + str(r.json()[strr]))
            geo_info += strr + ': ' + str(r.json()[strr]) + '    |    '
    return geo_info


def center_window_auto_full():
    # get the width and height of screen
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.geometry('%dx%d' %(ws, hs))


def center_window(w, h, window):
    # get the width and height of screen
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate x,y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


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

    txt_status.set('Upload: %5d %s' % (int(sent), unit) + '   Download: %5d %s' % (int(recv), unit) + '    |    ' + geo_info) # Update statusBar
    status.pack(side=BOTTOM, fill=X)
    analyze()
    global timer  # for recursively refreshing status bar and sniff data
    timer = threading.Timer(0, net_speed)
    timer.start()


def analyze():
    central_info.insert(END, bettercap.stdout.readline())
    central_info.see(END)


def quit():
    os.system('pkill bettercap')
    root.destroy()


def connect(id, pswd, window):
    contents = """
auto lo

iface lo inet loopback
iface eth0 inet dhcp

#auto eth0
auto wlan0
auto wlan1

iface wlan0 inet static
address 192.168.42.1
netmask 255.255.255.0
wireless-power off

up iptables-restore < /etc/iptables.ipv4.nat

allow-hotplug wlan1
iface wlan1 inet dhcp
"""

    with open('/etc/network/interfaces', 'w') as f:
        f.writelines(contents)
        f.write('\nwpa-ssid \"' + id + '\"\nwpa-psk \"' + pswd + '\"')
        f.close()
    window.destroy()


def create_window_connect(id):
    window_cnnct = tk.Toplevel(root)
    window_cnnct.title('Connect to an AP')
    center_window(int(root.winfo_screenwidth()), int(root.winfo_screenheight()), window_cnnct)
    frame_cnnct = Frame(window_cnnct)

    label_ap_name = Label(frame_cnnct, text='ESSID:' + id)
    label_ap_name.pack(side=TOP)

    label_pswd = Label(frame_cnnct, text='Password (if the ap is not encrypted, just click \"OK\"')
    label_pswd.pack(side=TOP)

    entry_pswd = Entry(frame_cnnct, width=int(root.winfo_screenwidth() / 30))
    entry_pswd.pack(side=TOP)

    btn_cnfrm = Button(frame_cnnct, text='OK', command=lambda: connect(id, entry_pswd.get(), window_cnnct))
    btn_cnfrm.pack(pady=int(root.winfo_screenwidth() / 60))

    frame_cnnct.pack(pady=int(root.winfo_screenwidth() / 40))

    window_cnnct.mainloop()


def create_window_aps():
    window_aps = tk.Toplevel(root)
    window_aps.title('Access Points')
    center_window(int(root.winfo_screenwidth()), int(root.winfo_screenheight()), window_aps)
    frame_aps = Scrollable(window_aps, width=25)
    output = subprocess.Popen(
        'iwlist wlan0 scan | grep -E \'ESSID|Quality|Group Cipher|Pairwise Ciphers|Authentication Suites\'',
        stdout=subprocess.PIPE, shell=True, universal_newlines=True).communicate()
    wlan_info = str(''.join(output[0]))
    wlan_info = wlan_info.replace('Quality', '\n\tQuality')
    list_aps = wlan_info.split('\t')
    btn_aps = []
    essid = []
    # print(len(list_aps))
    # for i in range(0, len(list_aps)):
    #     print(list_aps[i] + '\n------------------------------------------------------------\n')
    for i in range(1, len(list_aps)):
        essid.append(list_aps[i][list_aps[i].find('ESSID') + 7:list_aps[i].find('\"', list_aps[i].find('ESSID') + 7)])
        btn_aps.append(Button(frame_aps, text=list_aps[i], width=int(window_aps.winfo_screenwidth()), command=lambda i=i: create_window_connect(essid[i - 1])))
        # print(essid[i - 1])
        btn_aps[i - 1].pack(side=TOP)
    btn_close = Button(frame_aps, text='Close', width=int(window_aps.winfo_screenwidth()), command=window_aps.destroy)
    btn_close.pack(side=BOTTOM)
    frame_aps.update()
    window_aps.mainloop()


def show_status():
    output = subprocess.Popen('python3 status_analyze.py', stdout=subprocess.PIPE, shell=True, universal_newlines=True).communicate()
    central_info.insert(END, output[0])


# start from here


root = Tk()
buttonFont = font.Font(family='Helvetica', size=16, weight='bold')
central_infoFont = font.Font(family='Helvetica', size=16, weight='normal')
statusFont = font.Font(family='Helvetica', size=12, weight='normal')

center_window_auto_full()
root.title('Protector')
# root.overrideredirect(True)
# root.config(cursor="none")

frame_btns = Frame(root)
frame_center = Frame(root)

central_info = scrolledtext.ScrolledText(frame_center, relief=GROOVE, wrap=WORD, borderwidth=1, highlightthickness=0, font=central_infoFont)
central_info.pack(side=LEFT, expand=True, fill='both')
central_info.configure(bg='#2c2d3c', fg='white', padx=50, pady=50)

bettercap = subprocess.Popen('sudo bettercap', stdout=subprocess.PIPE, shell=True, universal_newlines=True)

txt_status = StringVar()
status = Label(root, textvariable=txt_status, relief=GROOVE, anchor=W, borderwidth=1, highlightthickness=0, font=statusFont)
status.pack(side=BOTTOM, fill=X)
status.configure(bg='black', fg='white')
geo_info = get_ip_info()
net_speed()

btn_wifi_browse = Button(frame_btns, text='Connect', borderwidth=1, highlightthickness=0, font=buttonFont, command=create_window_aps)
btn_wifi_browse.pack(side=LEFT, expand=True, fill='both')
btn_wifi_browse.configure(bg='black', fg='white')

btn_analyze = Button(frame_btns, text='Analyze', borderwidth=1, highlightthickness=0, font=buttonFont, command=net_speed)
btn_analyze.pack(side=LEFT, expand=True, fill='both')
btn_analyze.configure(bg='black', fg='white')

btn_Status = Button(frame_btns, text='Status', borderwidth=1, highlightthickness=0, font=buttonFont, command=show_status)
btn_Status.pack(side=LEFT, expand=True, fill='both')
btn_Status.configure(bg='black', fg='white')

btn_quit = Button(frame_btns, text='Quit', borderwidth=1, highlightthickness=0, font=buttonFont, command=quit)
btn_quit.pack(side=LEFT, expand=True, fill='both')
btn_quit.configure(bg='black', fg='white')

frame_btns.pack(side=LEFT, expand=True, fill='both')
frame_btns.place(relheight=0.25, relwidth=1)
frame_center.pack(expand=True, fill='both')
frame_center.place(rely=0.25, relheight=0.75, relwidth=1)

mainloop()
