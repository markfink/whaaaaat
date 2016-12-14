# -*- coding: utf-8 -*-
"""
`rawlist` type question
"""
from __future__ import print_function, unicode_literals
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.controls import TokenListControl
from prompt_toolkit.layout.containers import ConditionalContainer, \
    ScrollOffsets, HSplit
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.token import Token

from .. import PromptParameterException
from ..separator import Separator
from .common import setup_simple_validator, default_style
from .common import if_mousedown


# custom control based on TokenListControl

class InquirerControl(TokenListControl):
    def __init__(self, choices, **kwargs):
        self.pointer_index = 0
        self.answered = False
        self._init_choices(choices)
        super(InquirerControl, self).__init__(self._get_choice_tokens,
                                              **kwargs)

    def _init_choices(self, choices):
        self.choices = []  # list (key, name, value)
        # helper to convert from question format to internal format
        searching_first_choice = True
        key = 1  # used for numeric keys
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append(c)
            else:
                if isinstance(c, basestring):
                    self.choices.append((key, c, c))
                    key += 1
                #if 'value' in c:
                #    self.choices.append((c['name'], c['value']))
                #else:
                #    self.choices.append((c['name'], c['name']))
                #if 'checked' in c and c['checked']:
                #    self.selected_options.append(c['name'])
                if searching_first_choice:
                    self.pointer_index = i  # find the first choice
                    searching_first_choice = False

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self, cli):
        tokens = []
        T = Token

        def _append(index, line):
            if isinstance(line, Separator):
                tokens.append((T.Separator, '   %s\n' % line))
            else:
                key = line[0]
                line = line[1]
                pointed_at = (index == self.pointer_index)

                @if_mousedown
                def select_item(cli, mouse_event):
                    # bind option with this index to mouse event
                    self.pointer_index = index

                if pointed_at:
                    tokens.append((T.Selected, '  %d) %s' % (key, line),
                                   select_item))
                else:
                    tokens.append((T, '  %d) %s' % (key, line),
                                   select_item))

                tokens.append((T, '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            _append(i, choice)
        tokens.append((T, '  Answer: %d' % self.choices[self.pointer_index][0]))
        return tokens

    def get_selected_value(self):
        # get value not label
        return self.choices[self.pointer_index][2]


def question(message, **kwargs):
    # TODO extract common parts for list, checkbox, rawlist, expand
    if not 'choices' in kwargs:
        raise PromptParameterException('choices')
    # this does not implement default, use checked...
    # TODO
    #if 'default' in kwargs:
    #    raise ValueError('rawlist does not implement \'default\' '
    #                     'use \'checked\':True\' in choice!')

    choices = kwargs.pop('choices', None)

    # TODO style defaults on detail level
    style = kwargs.pop('style', default_style)

    ic = InquirerControl(choices)

    def get_prompt_tokens(cli):
        tokens = []
        T = Token

        tokens.append((Token.QuestionMark, '?'))
        tokens.append((Token.Question, ' %s ' % message))
        if ic.answered:
            tokens.append((Token.Answer, ' %s' % ic.get_selected_value()))
        return tokens

    # assemble layout
    layout = HSplit([
        Window(height=D.exact(1),
               content=TokenListControl(get_prompt_tokens, align_center=False)
        ),
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

    # add key bindings for choices
    #for i, c in enumerate(ic.choices):
    #    if not isinstance(c, Separator) and isinstance(c[2], int):
    #        key = c[2]
    #        @manager.registry.add_binding(key, eager=True)
    #        def toggle(event):
    #            pointed_choice = i

    @manager.registry.add_binding(Keys.Enter, eager=True)
    def set_answer(event):
        ic.answered = True
        event.cli.set_return_value(ic.get_selected_value())

    return Application(
        layout=layout,
        key_bindings_registry=manager.registry,
        mouse_support=True,
        style=style
    )
