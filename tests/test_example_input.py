# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import time
import textwrap

import pytest

from .helpers import keys
from .helpers import SimplePty


@pytest.fixture
def example_app():
    p = SimplePty.spawn(['python', 'examples/input.py'])
    yield p
    # it takes some time to collect the coverage data
    # if the main process exits too early the coverage data is not available
    time.sleep(p.delayafterterminate)
    p.sendintr()  # in case the subprocess was not ended by the test
    p.wait()  # without wait() the coverage info never arrives


def test_list(example_app):
    example_app.expect(textwrap.dedent("""\
        ? What's your first name  """))
    example_app.writeline('John')
    example_app.expect(textwrap.dedent("""\
        ? What's your first name  John
        ? What's your last name  Doe"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What's your last name  Doe
        ? What's your phone number  """))
    example_app.writeline('0123456789')
    example_app.expect(textwrap.dedent("""\
        ? What's your phone number  0123456789
        {
            "first_name": "John", 
            "last_name": "Doe", 
            "phone": "0123456789"
        }
        
        """))
