import ws_settings
from chat.ws import CLIENT_URL
import websocket
from lib.mylib_cls import Json

import chat.data.account


def exe(options, args):
    header = {"Type": "sender"}
    header.update(chat.data.account.DATA)
    ws = websocket.create_connection(options.URL, header=header)
    # add main process
    ws.send(str(Json(message=args[0])))


def options(parser):
    parser.add_option(
            "-u",
            "--url",
            dest="URL",
            default=ws_settings.URL + CLIENT_URL,
            help="connection url",
            )
    # add your options
