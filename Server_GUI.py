import os
import platform
import socket
import subprocess
import sys
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter.constants import *

import Server_GUI_Support


class Main_Window:

    def __init__(self, top=None):

        def Send():

            # Retrieve and encode the message

            message_to_client = self.Msg_box.get()
            message_to_client_encoded = message_to_client.encode('utf-8')

            # Send Message to client

            self.client.send(message_to_client_encoded)

            # Put the message in the text field

            self.Server_Msg.insert(
                END, message_to_client + "\t(" + datetime.now().strftime("%H:%M") + ")\n")

            # Put the time of latest message

            time = tk.StringVar()
            time.set("Last sent: "+datetime.now().strftime("%H:%M"))
            self.send_time.configure(textvariable=time)

            # Reset the message field

            blank = tk.StringVar()
            blank.set("")
            self.Msg_box.configure(textvariable=blank)

        def Recv():

            try:
                print("Try block")
                data = self.client.recv(self.max_size)
            except:
                print("No data received")

            if 'data' in locals():
                data_decoded = data.decode("utf-8")

                self.Client_Msg.insert(
                    END, data_decoded + "\t(" + datetime.now().strftime("%H:%M") + ")\n")

                time = tk.StringVar()
                time.set("Last received:" + datetime.now().strftime("%H:%M"))
                self.Recv_time.configure(textvariable=time)

            top.after(2000, Recv)

        '''Find Host IP and start listening'''

        self.operating_system = platform.system()

        if self.operating_system == "Windows":

            '''
            !!!!!!!!!!!!!!--------------WINDOWS USERS----------!!!!!!!!!!!!

            Set the number in below {self.findip} to the Network interface index of your NIC.

            Index can be obtained by: "netsh int ipv4 show interfaces"

            '''

            self.findip = "netsh interface ip show addresses 5".split()
            self.ip = subprocess.run(
                self.findip, stdout=subprocess.PIPE, universal_newlines=True)
            self.hostipindex = self.ip.stdout.split().index("Address:") + 1
            self.hostip = self.ip.stdout.split()[self.hostipindex]

        elif self.operating_system == "Linux":

            '''
            !!!!!!!!!!!!!!--------------LINUX USERS----------!!!!!!!!!!!!

            Set the adapter name after below 'ip addr show' to the adapter name
            used to host the server.

            Adapter Name can be obtained by: 'ifconfig'

            '''

            self.hostip = os.popen('ip addr show wlp3s0 | grep "\<inet\>"').read().split()[
                1].split('/')[0]

        ##########################################################

        self.HOST = self.hostip
        self.PORT = 6789  # Set port to any available port number
        self.max_size = 1024

        print("Server running on: ", self.HOST, ":", self.PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setblocking(0)
        self.sock.bind((self.HOST, self.PORT))

        print("Starting server at: ", datetime.now().strftime("%H:%M:%S"))
        print("Waiting for connections to connect...")

        self.sock.listen(5)
        self.client, self.address = self.sock.accept()
        self.client.setblocking(0)

        ##########################################################################

        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.', background=[
                       ('selected', _compcolor), ('active', _ana2color)])

        top.geometry("739x531+443+86")
        top.minsize(120, 1)
        top.maxsize(1359, 743)
        top.resizable(1,  1)
        top.title("Messenger (Server)")
        top.configure(background="#F9FFA4")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top

        self.Client_said = tk.Label(self.top)
        self.Client_said.place(relx=0.202, rely=0.202, height=33, width=58)
        self.Client_said.configure(activebackground="#f9f9f9")
        self.Client_said.configure(activeforeground="black")
        self.Client_said.configure(anchor='w')
        self.Client_said.configure(background="#F9FFA4")
        self.Client_said.configure(compound='left')
        self.Client_said.configure(disabledforeground="#a3a3a3")
        self.Client_said.configure(font="-family {Segoe UI} -size 10")
        self.Client_said.configure(foreground="#000000")
        self.Client_said.configure(highlightbackground="#d9d9d9")
        self.Client_said.configure(highlightcolor="black")
        self.Client_said.configure(text='''Client:''')

        self.Recv_time = tk.Label(self.top)
        self.Recv_time.place(relx=0.203, rely=0.368, height=22, width=154)
        self.Recv_time.configure(activebackground="#f9f9f9")
        self.Recv_time.configure(activeforeground="black")
        self.Recv_time.configure(anchor='w')
        self.Recv_time.configure(background="#F9FFA4")
        self.Recv_time.configure(compound='left')
        self.Recv_time.configure(disabledforeground="#a3a3a3")
        self.Recv_time.configure(font="-family {Fira Code Retina} -size 9")
        self.Recv_time.configure(foreground="#000000")
        self.Recv_time.configure(highlightbackground="#d9d9d9")
        self.Recv_time.configure(highlightcolor="black")

        self.Server_said = tk.Label(self.top)
        self.Server_said.place(relx=0.69, rely=0.433, height=32, width=45)
        self.Server_said.configure(activebackground="#f9f9f9")
        self.Server_said.configure(activeforeground="black")
        self.Server_said.configure(anchor='w')
        self.Server_said.configure(background="#F9FFA4")
        self.Server_said.configure(compound='left')
        self.Server_said.configure(disabledforeground="#a3a3a3")
        self.Server_said.configure(font="-family {Segoe UI} -size 10")
        self.Server_said.configure(foreground="#000000")
        self.Server_said.configure(highlightbackground="#d9d9d9")
        self.Server_said.configure(highlightcolor="black")
        self.Server_said.configure(text='''You:''')

        self.send_time = tk.Label(self.top)
        self.send_time.place(relx=0.555, rely=0.594, height=23, width=135)
        self.send_time.configure(activebackground="#ffff81")
        self.send_time.configure(activeforeground="black")
        self.send_time.configure(anchor='e')
        self.send_time.configure(background="#F9FFA4")
        self.send_time.configure(compound='left')
        self.send_time.configure(disabledforeground="#a3a3a3")
        self.send_time.configure(font="-family {Fira Code Retina} -size 9")
        self.send_time.configure(foreground="#000000")
        self.send_time.configure(highlightbackground="#d9d9d9")
        self.send_time.configure(highlightcolor="black")

        self.Send_btn = tk.Button(self.top)
        self.Send_btn.place(relx=0.758, rely=0.697, height=34, width=67)
        self.Send_btn.configure(activebackground="#ececec")
        self.Send_btn.configure(activeforeground="#000000")
        self.Send_btn.configure(background="#8080ff")
        self.Send_btn.configure(compound='left')
        self.Send_btn.configure(cursor="fleur")
        self.Send_btn.configure(disabledforeground="#a3a3a3")
        self.Send_btn.configure(foreground="#000000")
        self.Send_btn.configure(highlightbackground="#d9d9d9")
        self.Send_btn.configure(highlightcolor="black")
        self.Send_btn.configure(pady="0")
        self.Send_btn.configure(text='''Send''')
        self.Send_btn.configure(command=Send)

        self.Heading = tk.Label(self.top)
        self.Heading.place(relx=0.0, rely=0.0, height=51, width=744)
        self.Heading.configure(activebackground="#f9f9f9")
        self.Heading.configure(activeforeground="black")
        self.Heading.configure(background="#ff8040")
        self.Heading.configure(compound='left')
        self.Heading.configure(disabledforeground="#a3a3a3")
        self.Heading.configure(font="-family {Segoe UI} -size 14")
        self.Heading.configure(foreground="#000000")
        self.Heading.configure(highlightbackground="#d9d9d9")
        self.Heading.configure(highlightcolor="black")
        self.Heading.configure(relief="groove")
        self.Heading.configure(text='''Messenger (Server)''')

        self.Msg_box = tk.Entry(self.top)
        self.Msg_box.place(relx=0.217, rely=0.697, height=40, relwidth=0.52)
        self.Msg_box.configure(background="white")
        self.Msg_box.configure(disabledforeground="#a3a3a3")
        self.Msg_box.configure(
            font="-family {Neue Haas Grotesk Display Pro} -size 13")
        self.Msg_box.configure(foreground="#000000")
        self.Msg_box.configure(highlightbackground="#d9d9d9")
        self.Msg_box.configure(highlightcolor="black")
        self.Msg_box.configure(insertbackground="black")
        self.Msg_box.configure(selectbackground="blue")
        self.Msg_box.configure(selectforeground="white")

        self.Refresh = tk.Button(self.top)
        self.Refresh.place(relx=0.203, rely=0.885, height=24, width=57)
        self.Refresh.configure(activebackground="#ececec")
        self.Refresh.configure(activeforeground="#000000")
        self.Refresh.configure(background="#F24C4C")
        self.Refresh.configure(compound='left')
        self.Refresh.configure(disabledforeground="#a3a3a3")
        self.Refresh.configure(font="-family {Segoe UI} -size 9")
        self.Refresh.configure(foreground="#ffffff")
        self.Refresh.configure(highlightbackground="#d9d9d9")
        self.Refresh.configure(highlightcolor="black")
        self.Refresh.configure(pady="0")
        self.Refresh.configure(relief="solid")
        self.Refresh.configure(text='''Refresh''')
        self.Refresh.configure(command=Recv)

        self.Client_Msg = ScrolledText(self.top)
        self.Client_Msg.place(relx=0.203, rely=0.264,
                              relheight=0.105, relwidth=0.333)
        self.Client_Msg.configure(background="white")
        self.Client_Msg.configure(font="TkTextFont")
        self.Client_Msg.configure(foreground="black")
        self.Client_Msg.configure(highlightbackground="#d9d9d9")
        self.Client_Msg.configure(highlightcolor="black")
        self.Client_Msg.configure(insertbackground="black")
        self.Client_Msg.configure(insertborderwidth="3")
        self.Client_Msg.configure(selectbackground="blue")
        self.Client_Msg.configure(selectforeground="white")
        self.Client_Msg.configure(wrap="none")

        self.Server_Msg = ScrolledText(self.top)
        self.Server_Msg.place(relx=0.392, rely=0.49,
                              relheight=0.105, relwidth=0.333)
        self.Server_Msg.configure(background="white")
        self.Server_Msg.configure(font="TkTextFont")
        self.Server_Msg.configure(foreground="black")
        self.Server_Msg.configure(highlightbackground="#d9d9d9")
        self.Server_Msg.configure(highlightcolor="black")
        self.Server_Msg.configure(insertbackground="black")
        self.Server_Msg.configure(insertborderwidth="3")
        self.Server_Msg.configure(selectbackground="blue")
        self.Server_Msg.configure(selectforeground="white")
        self.Server_Msg.configure(wrap="none")

        top.after(2000, Recv)


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
            | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind(
            '<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped


class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>',
                       lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


def start_up():
    Server_GUI_Support.main()


if __name__ == '__main__':
    Server_GUI_Support.main()
