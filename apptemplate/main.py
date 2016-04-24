import ws_settings
import websocket
import json

# import <your app>.data.account


def exe(options, args):
    header = {"Type": "sender"}
    # your account data
    # header.update(<your app>.data.account.DATA)
    ws = websocket.create_connection(options.URL, header=header)
    # add main process


def options(parser):
    # add your options
