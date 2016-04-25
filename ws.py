import tornado.ioloop
import tornado.websocket
import django

import websocket
import threading
import ws_settings


class WebSocket(tornado.websocket.WebSocketHandler):
    clients = {}
    client_type = "sender"
    def check_origin(self, origin):
        print(origin)
        return True

    def open(self):
        self.client_type = self.request.headers.get("Type")
        self.username = WebSocket._extract_user(self)
        if self.client_type == "receiver":
            if not self.username in WebSocket.clients:
                WebSocket.clients[self.username] = []
            WebSocket.clients[self.username].append(self)
            print("websocket opened: " +self.username)
        self.client = self

    def on_close(self):
        if self.client_type == "receiver":
            WebSocket.del_client(self)
            print("websocket closed: " +self.request.headers["User"])

    def send_message(self, message):
        for client in WebSocket.get_client(self)[0]:
            client.write_message(str(message))

    @staticmethod
    def all_send_message(message):
        for clie in WebSocket.clients.values():
            for c in clie:
                c.write_message(str(message))

    def other_send_message(self, message):
        me = WebSocket.get_client(self)[0]
        for clie in WebSocket.clients.values():
            if clie != me:
                for c in clie:
                    c.write_message(str(message))

    @staticmethod
    def _extract_user(ws):
        return ws.request.headers["User"]

    @staticmethod
    def add_client(ws):
        username = WebSocket._extract_user(ws)
        if not username in WebSocket.clients:
            WebSocket.clients[username] = [ws]
        else:
            WebSocket.clients[username].append(ws)

    @staticmethod
    def del_client(ws):
        if ws.client_type != "closer":
            client, username = WebSocket.get_client(ws)
            ws.client_type = "closer"
            client.remove(ws)
            ws.close()
            if not client:
                del WebSocket.clients[username]

    @staticmethod
    def get_client(ws):
        username = WebSocket._extract_user(ws)
        return WebSocket.clients[username], username

    @staticmethod
    def get_user(data):
        user = data.get("user")
        return user if user else "guest"

    @staticmethod
    def get_account(data):
        pass


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
            client_data = __import__(i +".data.account")
            header = {"Type" : "receiver"}
            header.update(client_data.data.account.DATA)
            ws = websocket.create_connection("{0}{1}".format(
                ws_settings.URL,
                mod.ws.CLIENT_URL
                ), header=header)
            thread = mod.ws.WSThread(ws)
            thread.start()
            print(" === connect {} === ".format(i))
