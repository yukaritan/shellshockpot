from datetime import datetime
from flask import request


def _headers2dict(req: request) -> dict:
    """Grab the headers out of the request object and turn them into a dict"""

    return dict(req.headers.to_list())


def _printdict(data: dict, indentlevel=0, file=None):
    """A silly little utility to prettily print (nested) dicts"""

    outerindent = '    ' * indentlevel
    innerindent = '    ' * (indentlevel + 1)

    print(outerindent + '{', file=file)

    for k, v in data.items():
        if type(v) is dict:
            print('{innerindent}"{k}":'.format(innerindent=innerindent, k=k), file=file)
            _printdict(v, indentlevel=indentlevel+1, file=file)
        elif type(v) is list:
            print('{innerindent}"{k}": [{v}]'.format(innerindent=innerindent,
                                                     k=k,
                                                     v=' '.join('"%s"' % item for item in v)), file=file)
        else:
            print('{innerindent}"{k}": "{v}"'.format(innerindent=innerindent, k=k, v=v), file=file)

    print(outerindent + '}', file=file)


def _printreport(path, file=None):
    """I call print a thousand times here. I use it both to write to file and to print to the screen."""

    print("Time:", datetime.now(), file=file)
    print("Host:", request.remote_addr, file=file)
    print("Path: /" + path, file=file)
    print("Header:", file=file)
    _printdict(_headers2dict(request), file=file)

    data = dict(request.form)
    if data:
        print("POST:", file=file)
        _printdict(data, file=file)

    data = dict(request.args)
    if data:
        print("GET:", file=file)
        _printdict(data, file=file)

    data = request.get_json()
    if data:
        print("JSON:", file=file)
        _printdict(dict(data), file=file)

    print("---", file=file)


def log(fn):
    """Decorate a function with @decorators.log to add logging"""
    def wrapper(path, *args, **kw):
        with open('log.txt', 'a+') as logfile:
            _printreport(path, file=logfile)
        _printreport(path)
        return fn(path, *args, **kw)

    wrapper.__name__ = fn.__name__
    return wrapper
