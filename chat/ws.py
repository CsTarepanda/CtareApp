import ws
from chat import color_settings
from lib.linux.printer import inprint, cstr
import json

# your sever url
SERVER_URL = r"/chat/$"
class WebSocket(ws.WebSocket):
    def on_message(self, message):
        ws.WebSocket.all_send_message(message)


# connection url
CLIENT_URL = "/chat/"
class WSThread(ws.WSThread):
    def run(self):
        while self.run:
            data = json.loads(self.ws.recv(), "utf-8")
            inprint(cstr(data.get("message"), color_settings.MESSAGE))
