#!/usr/bin/python3
import websocket
ws = websocket.create_connection("ws://localhost:8080/todo/")

def tojson(string):
    result = '{'
    params = string.split()
    for i in params:
        line = i.split("=")
        result += '"{key}":"{value}",'.format(key=line[0], value=line[1])
    return result[:-1] + "}"
print("connect")
while True:
    ws.send(tojson(input("> ")))
