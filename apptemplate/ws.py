import ws

# your sever url
SERVER_URL = r""

class WebSocket(ws.WebSocket):
    def on_message(self, message):
        pass


# connection url
CLIENT_URL = ""
class WSThread(ws.WSThread):
    def run(self):
        pass
