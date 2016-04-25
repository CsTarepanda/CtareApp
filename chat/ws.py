import ws
from chat import color_settings
from lib.linux.printer import inprint, cstr
from lib.mylib_cls import Json
import json

# your sever url
SERVER_URL = r"/chat/$"
class WebSocket(ws.WebSocket):
    clients = {}

    def socket(self):
        return WebSocket

    def on_message(self, message):
        WebSocket.all_send_message(Json(
            message=message,
            username=self.username,
            ))


# connection url
CLIENT_URL = "/chat/"
class WSThread(ws.WSThread):
    def run(self):
        while self.run:
            data = json.loads(self.ws.recv(), "utf-8")
            inprint(cstr("{0}: {1}".format(
                data.get("username"),
                data.get("message"),
                ), color_settings.MESSAGE))
