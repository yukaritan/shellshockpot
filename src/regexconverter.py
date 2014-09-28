from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    """This simple class allows me to add regexes as routes"""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]