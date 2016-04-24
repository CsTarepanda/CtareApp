import ws
import json
from lib.mylib_cls import Sqlite3, Json
from lib.mylib_fnc import date_parse

SERVER_URL = r"/todo/$"

class WebSocket(ws.WebSocket):
    table = Sqlite3("todo/data/todo.sqlite3", dic=True).table("todo").create(
            "id integer primary key",
            "title unique not null",
            "todo not null",
            "done default 0",
            "date not null",
            )

    def on_message(self, message):
        try:
            data = json.loads(message, "utf-8")
            user = ws.WebSocket.get_user(data)
            password = data.get("password")
            connectuser = data.get("connect")
            if connectuser:
                self.client.send_message(Json(message="Hello, " + connectuser))
                self.other_send_message(Json(
                    message="connect by " + connectuser,
                    connectuser=connectuser,
                    ))
            else:
                title = data.get("title")
                todo = data.get("todo")
                date = data.get("date")
                func = data.get("func")
                if func == "list":
                    todolist = self.table.select(columns="title, todo, done, date", sql="where done==0")
                    self.send_message(Json(
                        message="list",
                        tododata=todolist
                        ))
                elif func == "all":
                    alltodolist = self.table.select(columns="title, todo, done, date")
                    self.send_message(Json(
                        message="all",
                        tododata=alltodolist
                        ))
                elif func == "save":
                    if title and todo and date:
                        self.table.insert(title=title, todo=todo, date=date_parse(date))
                        todo = self.table.select(
                                columns="title, todo, done, date",
                                sql="where title=='{}'".format(title)
                                )
                        ws.WebSocket.all_send_message(Json(
                            message="save",
                            tododata=todo,
                            ))
                    else:
                        self.send_message(Json(error="needs title, todo, date"))
                elif func == "done":
                    if title:
                        self.table.update("title=='{}'".format(title), done=1)
                        todo = self.table.select(
                                columns="title, todo, done, date",
                                sql="where title=='{}'".format(title)
                                )
                        ws.WebSocket.all_send_message(Json(
                            message="done",
                            tododata=todo,
                            ))
                    else:
                        self.send_message(Json(error="needs title"))
                elif func == "remove":
                    if title:
                        todo = self.table.select(
                                columns="title, todo, done, date",
                                sql="where title=='{}'".format(title)
                                )
                        self.table.delete("title=='{}'".format(title))
                        ws.WebSocket.all_send_message(Json(
                            message="remove",
                            tododata=todo,
                            ))
                    else:
                        self.send_message(Json(error="needs title"))
                elif func == "reopen":
                    if title:
                        self.table.update("title=='{}'".format(title), done=0)
                        todo = self.table.select(
                                columns="title, todo, done, date",
                                sql="where title=='{}'".format(title)
                                )
                        ws.WebSocket.all_send_message(Json(
                            message="reopen",
                            tododata=todo,
                            ))
                    else:
                        self.send_message(Json(error="needs title"))

        except Exception as e:
            ws.WebSocket.all_send_message(Json(error=str(e)))

from todo import color_settings
from lib.linux.printer import inprint, cstr

import getpass

CLIENT_URL = "/todo/"
class WSThread(ws.WSThread):
    def run(self):
        self.ws.send('{"connect":"'+getpass.getuser()+'"}')
        while self.run:
            data = json.loads(self.ws.recv(), "utf-8")
            if data.get("tododata"):
                inprint(cstr("=== {} ===".format(data.get("message")), color_settings.MESSAGE))
                for tododata in data.get("tododata"):
                    inprint(cstr("*{title}* {todo} {date}".format(
                        message = data.get("message"),
                        title = tododata.get("title"),
                        todo = tododata.get("todo"),
                        date = tododata.get("date"),
                        ), color_settings.DONE if tododata.get("done") else color_settings.TODO))
            else:
                inprint(cstr(data.get("message"), color_settings.MESSAGE))
            # data = json.loads(self.ws.recv(), "utf-8")
            # inprint(cstr(data.get("message"), color_settings.MESSAGE))
