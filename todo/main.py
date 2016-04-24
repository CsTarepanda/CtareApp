import ws_settings
import websocket
import todo.data.account
import json


def exe(options, args):
    header = {"Type": "sender"}
    header.update(todo.data.account.DATA)
    ws = websocket.create_connection(options.URL, header=header)
    data = {}
    data["title"] = options.TITLE
    data["todo"] = options.TODO
    data["date"] = options.DATE
    if options.ALL:
        data["func"] = "all"
    elif options.SAVE:
        data["func"] = "save"
    elif options.DONE:
        data["func"] = "done"
    elif options.REMOVE:
        data["func"] = "remove"
    elif options.REOPEN:
        data["func"] = "reopen"
    else:
        data["func"] = "list"
    ws.send(json.dumps(data, ensure_ascii=False))


def options(parser):
    parser.add_option(
            "-u",
            "--url",
            dest="URL",
            default=ws_settings.URL + "/todo/",
            help="connection url",
            )
    parser.add_option(
            "-a",
            "--all",
            dest="ALL",
            action="store_true",
            default=False,
            help="all todo"
            )
    parser.add_option(
            "-s",
            "--save",
            dest="SAVE",
            action="store_true",
            default=False,
            help="save todo"
            )
    parser.add_option(
            "-d",
            "--done",
            dest="DONE",
            action="store_true",
            default=False,
            help="done todo"
            )
    parser.add_option(
            "-r",
            "--remove",
            dest="REMOVE",
            action="store_true",
            default=False,
            help="remove todo"
            )
    parser.add_option(
            "-o",
            "--reopen",
            dest="REOPEN",
            action="store_true",
            default=False,
            help="reopen todo"
            )
    parser.add_option(
            "--title",
            dest="TITLE",
            help="title"
            )
    parser.add_option(
            "--todo",
            dest="TODO",
            help="todo"
            )
    parser.add_option(
            "--date",
            dest="DATE",
            help="deadline"
            )
