# -*- coding: utf-8 -*-
"""
Common test functionality
"""
import regex

from prompt_toolkit.eventloop.posix import PosixEventLoop
from prompt_toolkit.input import PipeInput
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.output import DummyOutput

from inquirer import style_from_dict, Token, prompt, print_json
from inquirer import prompts
from inquirer.utils import colorize_json, format_json


# http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/?in=user-97991
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

        # use Bunch to create group of variables:
        # cf = Bunch(datum=y, squared=y*y, coord=x)


keys = Bunch(
    DOWN='\x1b[B',
    UP='\x1b[A',
    LEFT='\x1b[D',
    RIGHT='\x1b[C',
    ENTER='\x0a',  # ControlJ  (Identical to '\n')
    ESCAPE='\x1b',
    CONTROLC='\x03',
    BACK='\x7f')


style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


def feed_app_with_input(type, message, text, **kwargs):
    """
    Create a CommandLineInterface, feed it with the given user input and return
    the CLI object.

    This returns a (result, CLI) tuple.
    note: this only works if you import your prompt and then this function!!
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


def remove_ansi_escape_sequences(text):
    # http://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    # also clean up the line endings
    return regex.sub(r'(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]|\ *\r', '', text)
