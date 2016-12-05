# -*- coding: utf-8 -*-
"""
`input` type question
"""
from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.shortcuts import create_prompt_application
from prompt_toolkit.validation import Validator, ValidationError

# use std prompt-toolkit control


def question(message, **kwargs):
    default = kwargs.pop('default', None)  # TODO
    validate_prompt = kwargs.pop('validate', None)
    if validate_prompt:
        if issubclass(validate_prompt, Validator):
            kwargs['validator'] = validate_prompt()
        elif callable(validate_prompt):
            class _InputValidator(Validator):
                def validate(self, document):
                    if not validate_prompt(document.text):
                        raise ValidationError(
                            message='invalid input',
                            cursor_position=len(document.text))
            kwargs['validator'] = _InputValidator()

    # TODO style defaults on detail level
    if not 'style' in kwargs:
        kwargs['style'] = style_from_dict({
            Token.QuestionMark: '#5F819D',
            #Token.Selected: '#FF9D00',  # AWS orange
            Token.Instruction: '',  # default
            Token.Answer: '#FF9D00 bold',  # AWS orange
            Token.Question: 'bold',
        })

    def _get_prompt_tokens(cli):
        tokens = []
        T = Token

        tokens.append((Token.QuestionMark, '?'))
        tokens.append((Token.Question, ' %s ' % message))
        #if ic.answered:
        #    tokens.append((Token.Answer, ' ' + ic.get_selection()))
        #else:
        #    tokens.append((Token.Instruction, ' (Use arrow keys)'))
        return tokens


    return create_prompt_application(
        get_prompt_tokens=_get_prompt_tokens, #refresh_interval=.5,
        **kwargs
    )
