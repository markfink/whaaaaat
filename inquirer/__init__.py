# -*- coding: utf-8 -*-

from __future__ import print_function
import os

from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict

from utils import print_json, format_json


__version__ = '0.1.3'


def here(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class PromptParameterException(Exception):
    def __init__(self, message, errors=None):

        # Call the base class constructor with the parameters it needs
        super(PromptParameterException, self).__init__(
            'You must provide a `%s` value' % message, errors)

from prompt import prompt
