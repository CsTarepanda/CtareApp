import ws_settings
# from <app name>.ws import CLIENT_URL
import websocket
from lib.mylib_cls import Json

# import <your app>.data.account


def exe(options, args):
    header = {"Type": "sender"}
    # your account data
    # header.update(<your app>.data.account.DATA)
    ws = websocket.create_connection(options.URL, header=header)
    # add main process


def options(parser):
    parser.add_option(
            "-u",
            "--url",
            dest="URL",
            default=ws_settings.URL + CLIENT_URL,
            help="connection url",
            )
    # add your options

