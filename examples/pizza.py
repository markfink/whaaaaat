# -*- coding: utf-8 -*-
"""
* Pizza delivery prompt example
* run example by writing `node pizza.js` in your console
"""

from inquirer import style_from_dict, Token, prompt, print_json


style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


print('Hi, welcome to Python Pizza')

questions = [
    {
        'type': 'confirm',
        'name': 'toBeDelivered',
        'message': 'Is this for delivery?',
        'default': False
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Large', 'Medium', 'Small'],
        'filter': lambda val : val.lower()
    },
    {
        'type': 'list',
        'name': 'freebie',
        'message': 'For a large pizza, you get a freebie',
        'choices': ['cake', 'fries'],
        'when': lambda answers : answers.size == 'large'
    }
]

answers = prompt(questions, style=style)
print('\nOrder receipt:')
print_json(answers)
