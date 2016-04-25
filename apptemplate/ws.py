import ws

# your sever url
SERVER_URL = r""

# your server
class WebSocket(ws.WebSocket):

    def socket(self):
        return WebSocket

    def on_message(self, message):
        pass


# connection url
CLIENT_URL = ""

# your client
class WSThread(ws.WSThread):
    def run(self):
        pass
