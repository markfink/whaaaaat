# -*- coding: utf-8 -*-
"""
* example for rawlist question type
* run example by typing `python example/checkbox.py` in your console
"""
from __future__ import print_function, unicode_literals

from whaaaaat import Style, prompt, print_json, Separator


style = Style.from_dict({
    'separator':    '#6C6C6C',
    'questionmark': '#FF9D00 bold',
    'selected':     '#5F819D',
    'pointer':      '#FF9D00 bold',
    'instruction':  '',  # default
    'answer':       '#5F819D bold',
    'question':     '',
})


questions = [
    {
        'type': 'rawlist',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask opening hours',
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'rawlist',
        'name': 'size',
        'message': 'What size do you need',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    }
]

answers = prompt(questions, style=style)
print_json(answers)
