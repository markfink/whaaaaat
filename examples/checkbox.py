# -*- coding: utf-8 -*-
"""
* Checkbox prompt example
* run example by typing `python example/checkbox.py` in your console
"""
from __future__ import print_function, unicode_literals

from inquirer import style_from_dict, Token, prompt, print_json


style = style_from_dict({
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
        'message': 'Select toppings',
        'name': 'toppings',
        'choices': [
            #new inquirer.Separator(' = The Meats = '),
            {
                'name': 'Ham'
            },
            {
                'name': 'Ground Meat'
            },
            {
                'name': 'Bacon'
            },
            #new inquirer.Separator(' = The Cheeses = '),
            {
                'name': 'Mozzarella',
                'checked': True
            },
            {
                'name': 'Cheddar'
            },
            {
                'name': 'Parmesan'
            },
            #new inquirer.Separator(' = The usual ='),
            {
                'name': 'Mushroom'
            },
            {
                'name': 'Tomato'
            },
            {
                'name': 'Pepperoni'
            },
            #new inquirer.Separator(' = The extras = '),
            {
                'name': 'Pineapple'
            },
            {
                'name': 'Olives',
                'disabled': 'out of stock'
            },
            {
                'name': 'Extra cheese'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=style)
print_json(answers)
