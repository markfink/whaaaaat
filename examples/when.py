# -*- coding: utf-8 -*-
"""
When example
"""
from __future__ import print_function, unicode_literals

from inquirer import style_from_dict, Token, prompt, print_json, default_style

style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


def dislikes_bacon(answers):
    # demonstrate use of a function... here a lambda function would be enough
    return not answers['bacon']


questions = [
    {
        'type': 'confirm',
        'name': 'bacon',
        'message': 'Do you like bacon?'
    },
    {
        'type': 'input',
        'name': 'favorite',
        'message': 'Bacon lover, what is your favorite type of bacon?',
        'when': lambda answers: answers['bacon']
    },
    {
        'type': 'confirm',
        'name': 'pizza',
        'message': 'Ok... Do you like pizza?',
        'when': dislikes_bacon
    },
    {
        'type': 'input',
        'name': 'favorite',
        'message': 'Whew! What is your favorite type of pizza?',
        'when': lambda answers: 'pizza' in answers
    }
]

answers = prompt(questions, style=default_style)

print_json(answers)
