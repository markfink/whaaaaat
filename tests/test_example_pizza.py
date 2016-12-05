# -*- coding: utf-8 -*-

import pytest
import pexpect

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


def _feed_app_with_input(type, name, message, text, **kwargs):
    """
    Create a CommandLineInterface, feed it with the given user input and return
    the CLI object.

    This returns a (result, CLI) tuple.
    """
    # If the given text doesn't end with a newline, the interface won't finish.
    assert text.endswith('\n')

    application = getattr(prompts, type).question(name, message,
                                                  **kwargs)

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


@pytest.fixture
def example_pizza():
    sut = pexpect.spawn('python examples/pizza.py')
    sut.expect('Hi, welcome to Python Pizza.*', timeout=1)
    yield sut


def test_select_first_choice(example_pizza):
    example_pizza.send(ENTER)
    example_pizza.expect('.*What size do you need.*', timeout=1)
    example_pizza.send(ENTER)
    example_pizza.expect('.*What size do you need.*', timeout=1)
    example_pizza.send(ENTER)
    example_pizza.expect(
        '.*For a large pizza, you get a freebie.*(Use arrow keys)*', timeout=1)
    example_pizza.send(ENTER)
    example_pizza.expect('.*Order receipt.*', timeout=1)
