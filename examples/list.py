# -*- coding: utf-8 -*-
"""
list prompt example
"""
from __future__ import print_function, unicode_literals

from whaaaaat import Style, prompt, print_json, default_style,\
    Separator

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
        'type': 'list',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask for opening hours',
            {
                'name': 'Contact support',
                'disabled': 'Unavailable at this time'
            },
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    }
]

answers = prompt(questions, style=style)
print_json(answers)
