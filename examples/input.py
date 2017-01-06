# -*- coding: utf-8 -*-
"""
* Input prompt example
* run example by writing `python example/input.py` in your console
"""
from __future__ import print_function, unicode_literals
import regex

from whaaaaat import style_from_dict, Token, prompt, print_json
from whaaaaat import Validator, ValidationError, default_style


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
        'default': 'John'
    },
    {
        'type': 'input',
        'name': 'last_name',
        'message': 'What\'s your last name',
        'validate': lambda val: val == 'Doe' or 'is your name Doe?'
    },
    {
        'type': 'input',
        'name': 'phone',
        'message': 'What\'s your phone number',
        'validate': PhoneNumberValidator
    }
]

answers = prompt(questions, style=default_style)
print_json(answers)
