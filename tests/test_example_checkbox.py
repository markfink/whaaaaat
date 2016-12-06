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

from .helpers import feed_app_with_input, keys



@pytest.fixture
def example_checkbox():
    sut = pexpect.spawn('python examples/checkbox.py')
    sut.expect('Hi, welcome to Python Pizza.*', timeout=1)
    yield sut

# FIXME
def test_select_first_choice(example_checkbox):
    example_checkbox.send(keys.ENTER)
    example_checkbox.expect('.*What size do you need.*', timeout=1)
    example_checkbox.send(keys.ENTER)
    example_checkbox.expect('.*What size do you need.*', timeout=1)
    example_checkbox.send(keys.ENTER)
    example_checkbox.expect(
        '.*For a large pizza, you get a freebie.*(Use arrow keys)*', timeout=1)
    example_checkbox.send(keys.ENTER)
    example_checkbox.expect('.*Order receipt.*', timeout=1)
