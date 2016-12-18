# -*- coding: utf-8 -*-
from __future__ import print_function
import json

from pygments import highlight, lexers, formatters

__version__ = '0.1.2'


def format_json(data):
    return json.dumps(data, sort_keys=True, indent=4)


def colorize_json(data):
    colorful_json = highlight(unicode(data, 'UTF-8'),
                              lexers.JsonLexer(),
                              formatters.TerminalFormatter())
    return colorful_json


def print_json(data):
    #colorful_json = highlight(unicode(format_json(data), 'UTF-8'),
    #                          lexers.JsonLexer(),
    #                          formatters.TerminalFormatter())
    print(colorize_json(format_json(data)))
