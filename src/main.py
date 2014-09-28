#!/usr/bin/env python3.4
from datetime import datetime

from flask import Flask, request

from regexconverter import RegexConverter


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


def headers2dict(req: request) -> dict:
    """Grab the headers out of the request object and turn them into a dict"""

    return dict(req.headers.to_list())


def printdict(data: dict, indentlevel=0, file=None):
    """A silly little utility to prettily print (nested) dicts"""

    outerindent = '    ' * indentlevel
    innerindent = '    ' * (indentlevel + 1)

    print(outerindent + '{', file=file)

    for k, v in data.items():
        if type(v) is dict:
            print('{innerindent}"{k}":'.format(innerindent=innerindent, k=k), file=file)
            printdict(v, indentlevel=indentlevel+1, file=file)
        else:
            print('{innerindent}"{k}": "{v}"'.format(innerindent=innerindent, k=k, v=v), file=file)

    print(outerindent + '}', file=file)


def printreport(path, file=None):
    """I call print a thousand times here. I use it both to write to file and to print to the screen."""

    print("Time:", datetime.now(), file=file)
    print("Host:", request.remote_addr, file=file)
    print("Path: /" + path, file=file)
    printdict(headers2dict(request), file=file)
    print("---", file=file)


@app.route('/<regex(".*"):path>')
def landing(path: str):
    """With the above regex, this function will be hit no matter what path you try."""

    with open('log.txt', 'a+') as log:
        printreport(path, file=log)
    printreport(path)
    return 'some response here'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
