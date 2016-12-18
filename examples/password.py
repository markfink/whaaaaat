# -*- coding: utf-8 -*-
"""
* password prompt example
"""
from __future__ import print_function, unicode_literals

from inquirer import prompt, print_json, default_style


questions = [
    {
        'type': 'password',
        'message': 'Enter your git password',
        'name': 'password'
    }
]

answers = prompt(questions, style=default_style)
print_json(answers)
