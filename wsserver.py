import tornado.ioloop
import tornado.websocket
import django
import os
import json


class WebSocket(tornado.websocket.WebSocketHandler):
    clients = []
    def check_origin(self, origin):
        print(origin)
        return True

    def open(self):
        TodoWebSocket.clients.append(self)
        print("websocket opened")

    def on_close(self):
        TodoWebSocket.clients.remove(self)
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

class TodoWebSocket(WebSocket):
    def on_message(self, message):
        try:
            data = json.loads(message, "utf-8")
            user = data.get("user")
            user = user if user else "no name"
            psw = data.get("pass")
            msg = data.get("msg")
            connectuser = data.get("connect")
            if connectuser:
                self.send_message("Hello, " + connectuser)
                self.other_send_message("connect by " + connectuser)
            else:
                WebSocket.all_send_message(str(msg) + " by " + user)
        except Exception as e:
            print(e)
            WebSocket.all_send_message(str(e))

application = tornado.web.Application([
    (r'/todo/$', TodoWebSocket),
])

if __name__ == "__main__":
    application.listen(8080)
    print("runserver: localhost:8080")
    tornado.ioloop.IOLoop.instance().start()
