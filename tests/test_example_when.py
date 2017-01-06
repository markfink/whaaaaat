# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import time
import textwrap

import pytest

from .helpers import keys
from .helpers import SimplePty


@pytest.fixture
def example_app():
    p = SimplePty.spawn(['python', 'examples/when.py'])
    yield p
    # it takes some time to collect the coverage data
    # if the main process exits too early the coverage data is not available
    time.sleep(p.delayafterterminate)
    p.sendintr()  # in case the subprocess was not ended by the test
    p.wait()  # without wait() the coverage info never arrives


def test_when_bacon(example_app):
    example_app.expect('? Do you like bacon?  (Y/n)')
    example_app.write(keys.ENTER)

    example_app.expect(textwrap.dedent("""\
        ? Do you like bacon?  Yes
        ? Bacon lover, what is your favorite type of bacon? """))
    example_app.writeline('smoked bacon')
    example_app.expect(textwrap.dedent("""\
        ? Bacon lover, what is your favorite type of bacon? smoked bacon
        {
            "bacon": true, 
            "favorite": "smoked bacon"
        }
        
        """))


def test_when_pizza(example_app):
    example_app.expect('? Do you like bacon?  (Y/n)')
    example_app.write('n')

    example_app.expect(textwrap.dedent("""\
        ? Do you like bacon?  No
        ? Ok... Do you like pizza?  (y/N)"""))
    example_app.write('y')

    example_app.expect(textwrap.dedent("""\
        ? Ok... Do you like pizza?  Yes
        ? Whew! What is your favorite type of pizza? """))
    example_app.writeline('Toscana')

    example_app.expect(textwrap.dedent("""\
        ? Whew! What is your favorite type of pizza? Toscana
        {
            "bacon": false, 
            "favorite": "Toscana", 
            "pizza": true
        }
        
        """))


def test_when_no_thanks(example_app):
    example_app.expect('? Do you like bacon?  (Y/n)')
    example_app.write('n')

    example_app.expect(textwrap.dedent("""\
        ? Do you like bacon?  No
        ? Ok... Do you like pizza?  (y/N)"""))
    example_app.write('n')

    example_app.expect(textwrap.dedent("""\
        ? Ok... Do you like pizza?  No
        {
            "bacon": false, 
            "pizza": false
        }
        
        """))
