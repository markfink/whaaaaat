# -*- coding: utf-8 -*-

from prompt_toolkit.eventloop.posix import PosixEventLoop
from prompt_toolkit.input import PipeInput
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.output import DummyOutput

from inquirer import style_from_dict, Token, prompt, print_json
from inquirer import prompts
from inquirer.prompts import list


DOWN =     '\x1b[B'
UP =       '\x1b[A'
LEFT =     '\x1b[D'
RIGHT =    '\x1b[C'
ENTER =    '\x0a'  # ControlJ  (Identical to '\n')
ESCAPE =   '\x1b'
CONTROLC = '\x03'
BACK =     '\x7f'


style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


def _feed_app_with_input(type, message, text, **kwargs):
    """
    Create a CommandLineInterface, feed it with the given user input and return
    the CLI object.

    This returns a (result, CLI) tuple.
    """
    # If the given text doesn't end with a newline, the interface won't finish.
    assert text.endswith('\n')

    application = getattr(prompts, type).question(message, **kwargs)

    loop = PosixEventLoop()
    try:
        inp = PipeInput()
        inp.send_text(text)
        cli = CommandLineInterface(
            application=application,
            eventloop=loop,
            input=inp,
            output=DummyOutput())
        result = cli.run()
        return result, cli
    finally:
        loop.close()
        inp.close()


def test_select_first_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    #text = DOWN + ENTER
    text = ENTER

    result, cli = _feed_app_with_input('list', message, text, **kwargs)
    assert result == 'foo'


def test_select_second_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = DOWN + ENTER

    result, cli = _feed_app_with_input('list', message, text, **kwargs)
    assert result == 'bar'


def test_select_third_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = DOWN + DOWN + ENTER

    result, cli = _feed_app_with_input('list', message, text, **kwargs)
    assert result == 'bazz'


def test_cycle_to_first_choice():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = DOWN + DOWN + DOWN + ENTER

    result, cli = _feed_app_with_input('list', message, text, **kwargs)
    assert result == 'foo'


def test_cycle_backwards():
    message = 'Foo message'
    name = 'Bar variable'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = UP + ENTER

    result, cli = _feed_app_with_input('list', message, text, **kwargs)
    assert result == 'bazz'


# TODO number shortcuts + tests from Inquirer.js
