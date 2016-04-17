import ws
import json

SERVER_URL = r"/todo/$"

class WebSocket(ws.WebSocket):
    def on_message(self, message):
        try:
            data = json.loads(message, "utf-8")
            user = ws.WebSocket.get_user(data)
            msg = data.get("msg")
            connectuser = data.get("connect")
            if connectuser:
                self.send_message("Hello, " + connectuser)
                self.other_send_message("connect by " + connectuser)
            else:
                ws.WebSocket.all_send_message(str(msg) + " by " + user)
        except Exception as e:
            ws.WebSocket.all_send_message(str(e))

from todo import color_settings
from lib.mylib_fnc import inprint, cstr

import getpass

CLIENT_URL = "/todo/"
class WSThread(ws.WSThread):
    def run(self):
        self.ws.send('{"connect":"'+getpass.getuser()+'"}')
        while self.run:
            inprint(cstr(self.ws.recv(), color_settings.MESSAGE))
