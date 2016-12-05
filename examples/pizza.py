# -*- coding: utf-8 -*-
"""
* Pizza delivery prompt example
* run example by writing `python example/pizza.py` in your console
"""
from __future__ import print_function, unicode_literals
import regex

from inquirer import style_from_dict, Token, prompt, print_json
from inquirer import Validator, ValidationError


style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


print('Hi, welcome to Python Pizza')

questions = [
    {
        'type': 'confirm',
        'name': 'toBeDelivered',
        'message': 'Is this for delivery?',
        'default': False
    },
    {
        'type': 'input',
        'name': 'phone',
        'message': 'What\'s your phone number?',
        'validate': PhoneNumberValidator
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Large', 'Medium', 'Small'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'list',
        'name': 'freebie',
        'message': 'For a large pizza, you get a freebie',
        'choices': ['cake', 'fries'],
        'when': lambda answers: answers['size'] == 'large'
    }
]

answers = prompt(questions, style=style)
print('\nOrder receipt:')
print_json(answers)
