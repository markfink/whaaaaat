# -*- coding: utf-8 -*-
"""
`list` type question
"""
from __future__ import print_function
from __future__ import unicode_literals
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.controls import TokenListControl
from prompt_toolkit.layout.containers import ConditionalContainer, \
    ScrollOffsets, HSplit
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.mouse_events import MouseEventTypes
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict

from .. import PromptParameterException


# custom control based on TokenListControl
# docu here:
# https://github.com/jonathanslenders/python-prompt-toolkit/issues/281
# https://github.com/jonathanslenders/python-prompt-toolkit/blob/master/examples/full-screen-layout.py
# https://github.com/jonathanslenders/python-prompt-toolkit/blob/master/docs/pages/full_screen_apps.rst


def if_mousedown(handler):
    def handle_if_mouse_down(cli, mouse_event):
        if mouse_event.event_type == MouseEventTypes.MOUSE_DOWN:
            return handler(cli, mouse_event)
        else:
            return NotImplemented

    return handle_if_mouse_down


class InquirerControl(TokenListControl):
    selected_option_index = 0
    answered = False
    choices = []

    def __init__(self, choices, **kwargs):
        self.choices = choices
        super(InquirerControl, self).__init__(self._get_choice_tokens,
                                              **kwargs)

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self, cli):
        tokens = []
        T = Token

        def append(index, label):
            selected = (index == self.selected_option_index)

            @if_mousedown
            def select_item(cli, mouse_event):
                # bind option with this index to mouse event
                self.selected_option_index = index
                self.answered = True
                cli.set_return_value(None)

            token = T.Selected if selected else T

            tokens.append((T.Selected if selected else T, ' > ' if selected
            else '   '))
            if selected:
                tokens.append((Token.SetCursorPosition, ''))

            tokens.append((T.Selected if selected else T, '%-24s' % label,
                           select_item))
            tokens.append((T, '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()  # Remove last newline.
        return tokens

    def get_selection(self):
        return self.choices[self.selected_option_index]


def question(message, **kwargs):
    if not 'choices' in kwargs:
        raise PromptParameterException('choices')

    choices = kwargs.pop('choices', None)
    default = kwargs.pop('default', 0)  # TODO

    # TODO style defaults on detail level
    style = kwargs.pop('style', style_from_dict({
        Token.QuestionMark: '#5F819D',
        Token.Selected: '#FF9D00',  # AWS orange
        Token.Instruction: '',  # default
        Token.Answer: '#FF9D00 bold',  # AWS orange
        Token.Question: 'bold',
    }))

    ic = InquirerControl(choices)

    def get_prompt_tokens(cli):
        tokens = []
        T = Token

        tokens.append((Token.QuestionMark, '?'))
        tokens.append((Token.Question, ' %s ' % message))
        if ic.answered:
            tokens.append((Token.Answer, ' ' + ic.get_selection()))
        else:
            tokens.append((Token.Instruction, ' (Use arrow keys)'))
        return tokens

    # assemble layout
    layout = HSplit([
        Window(height=D.exact(1),
               content=TokenListControl(get_prompt_tokens, align_center=False)),
        ConditionalContainer(
            Window(
                ic,
                width=D.exact(43),
                height=D(min=3),
                scroll_offsets=ScrollOffsets(top=1, bottom=1)
            ),
            filter=~IsDone()
        )
    ])

    # key bindings
    manager = KeyBindingManager.for_prompt()

    @manager.registry.add_binding(Keys.ControlQ, eager=True)
    @manager.registry.add_binding(Keys.ControlC, eager=True)
    def _(event):
        raise KeyboardInterrupt()
        # event.cli.set_return_value(None)

    @manager.registry.add_binding(Keys.Down, eager=True)
    def move_cursor_down(event):
        ic.selected_option_index = (
            (ic.selected_option_index + 1) % ic.choice_count)

    @manager.registry.add_binding(Keys.Up, eager=True)
    def move_cursor_up(event):
        ic.selected_option_index = (
            (ic.selected_option_index - 1) % ic.choice_count)

    @manager.registry.add_binding(Keys.Enter, eager=True)
    def set_answer(event):
        ic.answered = True
        event.cli.set_return_value(ic.get_selection())

    return Application(
        layout=layout,
        key_bindings_registry=manager.registry,
        mouse_support=True,
        style=style
    )
