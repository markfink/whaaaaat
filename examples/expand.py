# -*- coding: utf-8 -*-
"""
* example for expand question type
* run example by typing `python example/checkbox.py` in your console
"""
from __future__ import print_function, unicode_literals

from inquirer import style_from_dict, Token, prompt, print_json, Separator


style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '',  # default
    Token.Pointer: '#FF9D00 bold',  # AWS orange
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'checkbox',
        'message': 'Conflict on `file.js`: ',
        'name': 'overwrite',
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
