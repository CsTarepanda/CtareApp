#!/usr/bin/python3
import websocket
import threading
from lib.mylib_fnc import cstr, inprint
from todo.app import color_settings


class WSThread(threading.Thread):
    run = True
    def __init__(self, ws):
        super(WSThread, self).__init__()
        self.ws = ws

    def run(self):
        while self.run:
            inprint(cstr(self.ws.recv()), color_settings.MESSAGE)

    def close(self):
        self.run = False

ws = websocket.create_connection("ws://localhost:8080/todo/")
thread = WSThread(ws)
thread.start()
print(" === connect === ")
import getpass
ws.send('{"connect":"'+getpass.getuser()+'"}')
