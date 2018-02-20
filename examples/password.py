# -*- coding: utf-8 -*-
"""
* password question example
"""
from __future__ import print_function, unicode_literals

from whaaaaat import Style, prompt, print_json


style = Style.from_dict({
    'questionmark': '#FF9D00 bold',
    'instruction':  '',  # default
    'answer':       '#5F819D bold',
    'question':     '',
})


questions = [
    {
        'type': 'password',
        'message': 'Enter your git password',
        'name': 'password'
    }
]

answers = prompt(questions, style=style)
print_json(answers)
