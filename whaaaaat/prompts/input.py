# -*- coding: utf-8 -*-
"""
`input` type question
"""
from __future__ import print_function, unicode_literals
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.lexers.base import SimpleLexer
from prompt_toolkit.shortcuts.prompt import prompt, Prompt

from .common import default_style


def question(message, **kwargs):
    #default = kwargs.pop('default', '')
    validate_prompt = kwargs.pop('validate', None)
    input = kwargs.pop('input', None)
    output = kwargs.pop('output', None)
    if validate_prompt:
        if issubclass(validate_prompt, Validator):
            kwargs['validator'] = validate_prompt()
        elif callable(validate_prompt):
            class _InputValidator(Validator):
                def validate(self, document):
                    verdict = validate_prompt(document.text)
                    if not verdict == True:
                        if verdict == False:
                            verdict = 'invalid input'
                        raise ValidationError(
                            message=verdict,
                            cursor_position=len(document.text))
            kwargs['validator'] = _InputValidator()

    # TODO style defaults on detail level
    kwargs['style'] = kwargs.pop('style', default_style)

    def _get_prompt():
        return [
            ('class:questionmark', '?'),
            ('class:question', ' %s  ' % message)
        ]

    #print(kwargs)
    #return prompt(_get_prompt,
    #    lexer=SimpleLexer('class:answer'),
    #    **kwargs
    #)
    prompt = Prompt(input=input, output=output)
    return prompt.prompt(_get_prompt,
         lexer=SimpleLexer('class:answer'),
         **kwargs
    )

#return app.run(inputhook)


'''
def _assemble_app_using_prompt(
        message=None,
        # When any of these arguments are passed, this value is overwritten
        # for the current prompt.
        default='', editing_mode=None,
        refresh_interval=None, vi_mode=None, lexer=None, completer=None,
        complete_in_thread=None, is_password=None, extra_key_bindings=None,
        bottom_toolbar=None, style=None, include_default_pygments_style=None,
        rprompt=None, multiline=None, prompt_continuation=None,
        wrap_lines=None, history=None, enable_history_search=None,
        complete_while_typing=None, validate_while_typing=None,
        complete_style=None, auto_suggest=None, validator=None,
        clipboard=None, mouse_support=None, extra_input_processor=None,
        reserve_space_for_menu=None, enable_system_prompt=None,
        enable_suspend=None, enable_open_in_editor=None,
        tempfile_suffix=None, inputhook=None,
        async_=False):
    """ The global `prompt` function. This will create a new `Prompt` instance
    for every call.  """
    prompt = Prompt()
    #prompt.prompt(*a, **kw)

    # Take settings from 'prompt'-arguments.
    for name in prompt._fields:
        value = locals()[name]
        if value is not None:
            setattr(prompt, name, value)

    return prompt.app, prompt.inputhook
'''
