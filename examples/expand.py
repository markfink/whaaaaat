# -*- coding: utf-8 -*-
"""
* example for expand question type
* run example by typing `python example/checkbox.py` in your console
"""
from __future__ import print_function, unicode_literals

from whaaaaat import Style, prompt, print_json, Separator


style = Style.from_dict({
    'separator':     '#6C6C6C',
    'questionmark':  '#FF9D00 bold',
    #Token.Selected: '',  # default
    'selected':      '#5F819D',
    'pointer':       '#FF9D00 bold',
    'instruction':   '',  # default
    'answer':        '#5F819D bold',
    'question':      '',
})


questions = [
    {
        'type': 'expand',
        'message': 'Conflict on `file.js`: ',
        'name': 'overwrite',
        'default': 'a',
        'choices': [
            {
                'key': 'y',
                'name': 'Overwrite',
                'value': 'overwrite'
            },
            {
                'key': 'a',
                'name': 'Overwrite this one and all next',
                'value': 'overwrite_all'
            },
            {
                'key': 'd',
                'name': 'Show diff',
                'value': 'diff'
            },
            Separator(),
            {
                'key': 'x',
                'name': 'Abort',
                'value': 'abort'
            }
        ]
    }
]

answers = prompt(questions, style=style)
print_json(answers)
