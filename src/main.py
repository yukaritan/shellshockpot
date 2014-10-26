#!/usr/bin/env python3.4

from flask import Flask, request
from regexconverter import RegexConverter
import decorators

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


@app.route('/robots.txt')
def robotstxt():
    """Tell crawlers to piss off"""
    return open('src/robots.txt', 'r').read()


@app.route('/your-detectify-id-here.txt')
def detectify():
    """In case you're running detectify"""
    return "detectify"


@app.route('/<regex(".*phpMyAdmin.*"):path>', methods=('GET', 'POST'))
@app.route('/<regex(".*mysqladmin.*"):path>', methods=('GET', 'POST'))
@app.route('/<regex(".*pma.*"):path>', methods=('GET', 'POST'))
@app.route('/<regex(".*MyAdmin.*"):path>', methods=('GET', 'POST'))
@app.route('/<regex(".*myadmin.*"):path>', methods=('GET', 'POST'))
@decorators.log
def phpmyadmin(path: str):
    """Pretend to be phpMyAdmin"""
    return open('responses/phpMyAdmin-2.11.11.3.txt', 'r').read()


@app.route('/<regex(".*wp-login\.php.*"):path>', methods=('GET', 'POST'))
@decorators.log
def wordpress(path: str):
    """Pretend to be wp-login.php"""
    return open('responses/wordpress.txt', 'r').read()


@app.route('/<regex(".*"):path>', methods=('GET', 'POST'))
@decorators.log
def landing(path: str):
    """With the above regex, this function will be hit no matter what path you try."""

    if 'bingbot' in request.headers.get('User-Agent'):
        return robotstxt()

    return 'some response here'  # this is where we stick our bait!
                                 # well, unless we come up with some better regexes.. regexii? regii?


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
