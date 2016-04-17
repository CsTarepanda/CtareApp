import tornado.ioloop
import tornado.websocket
import django

import websocket
import threading
import ws_settings


class WebSocket(tornado.websocket.WebSocketHandler):
    clients = []
    def check_origin(self, origin):
        print(origin)
        return True

    def open(self):
        WebSocket.clients.append(self)
        print("websocket opened")

    def on_close(self):
        WebSocket.clients.remove(self)
        print("websocket closed")

    def send_message(self, message):
        self.write_message(message)

    @staticmethod
    def all_send_message(message):
        for clie in WebSocket.clients:
            clie.write_message(message)

    def other_send_message(self, message):
        for clie in WebSocket.clients:
            if clie != self:
                clie.write_message(message)

    @staticmethod
    def get_user(data):
        user = data.get("user")
        return user if user else "guest"


class WSThread(threading.Thread):
    run = True
    def __init__(self, ws):
        super(WSThread, self).__init__()
        self.ws = ws

    def close(self):
        self.run = False


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print("server or client")
    elif sys.argv[1] == "server":
        wsservers = []
        for i in ws_settings.SERVERS:
            mod = __import__(i +".ws")
            wsservers.append((mod.ws.SERVER_URL, mod.ws.WebSocket))
        application = tornado.web.Application(wsservers)

        application.listen(8080)
        print("runserver: " + ws_settings.URL)
        print("run apps:\n - {}".format("\n - ".join(ws_settings.SERVERS)))
        tornado.ioloop.IOLoop.instance().start()

    elif sys.argv[1] == "client":
        THREADS = []
        for i in ws_settings.CLIENTS:
            mod = __import__(i +".ws")
            ws = websocket.create_connection("{0}{1}".format(
                ws_settings.URL,
                mod.ws.CLIENT_URL
                ))
            thread = mod.ws.WSThread(ws)
            thread.start()
            print(" === connect {} === ".format(i))
