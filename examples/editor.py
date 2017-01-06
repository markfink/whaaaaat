# -*- coding: utf-8 -*-
"""
* Editor prompt example
"""
from __future__ import print_function, unicode_literals

from whaaaaat import style_from_dict, Token, prompt, print_json
from whaaaaat import Validator, ValidationError, default_style


questions = [
    {
        'type': 'editor',
        'name': 'bio',
        'message': 'Please write a short bio of at least 3 lines.',
        'validate': lambda text: len(text.split('\n')) >= 3 or 'Must be at least 3 lines.'
    }
]

answers = prompt(questions, style=default_style)
print_json(answers)
