# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import time
import textwrap

import pytest

from prompt_toolkit.eventloop.posix import PosixEventLoop
from prompt_toolkit.input import PipeInput
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.output import DummyOutput

from whaaaaat import style_from_dict, Token, prompt, print_json
from whaaaaat import prompts
from whaaaaat.prompts import list

from .helpers import feed_app_with_input, keys
from .helpers import SimplePty


@pytest.fixture
def example_app():
    p = SimplePty.spawn(['python', 'examples/checkbox.py'])
    yield p
    # it takes some time to collect the coverage data
    # if the main process exits too early the coverage data is not available
    time.sleep(p.delayafterterminate)
    p.sendintr()  # in case the subprocess was not ended by the test
    p.wait()  # without wait() the coverage info never arrives


def test_checkbox(example_app):
    # test the helper class plus demonstrate how to use it...
    #with pytest.raises(AssertionError):
    example_app.expect(textwrap.dedent("""\
        ? Select toppings  (<up>, <down> to move, <space> to select, <a> to toggle, <i> 
         = The Meats =
         ❯○ Ham
          ○ Ground Meat
          ○ Bacon
         = The Cheeses =
          ● Mozzarella
          ○ Cheddar
          ○ Parmesan
         = The usual =
          ○ Mushroom
          ○ Tomato
          ○ Pepperoni
         = The extras =
          ○ Pineapple
          ○ Olives
          ○ Extra cheese"""))
    #example_app.write('\n')
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Select toppings  [Mozzarella]
        {
            "toppings": [
                "Mozzarella"
            ]
        }
        
        """))


'''
def test_checkbox(example_app):
    # test the helper class plus demonstrate how to use it...
    example_app.writeline('Stuart')
    assert example_app == textwrap.dedent("""\
        hi, there!""")
    example_app.write(' ')
    assert example_app == textwrap.dedent("""\
        hi, there!""")
    example_app.write('\n')
    assert example_app == textwrap.dedent("""\
        ? Select toppings  done (2 selections)
        {
            "toppings": [
                "Ham",
                "Mozzarella"
            ]
        }""")
'''


'''
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
'''
