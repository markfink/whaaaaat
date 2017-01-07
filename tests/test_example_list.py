# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import time
import textwrap

import pytest

from .helpers import keys
from .helpers import SimplePty


@pytest.fixture
def example_app():
    p = SimplePty.spawn(['python', 'examples/list.py'])
    yield p
    # it takes some time to collect the coverage data
    # if the main process exits too early the coverage data is not available
    time.sleep(p.delayafterterminate)
    p.sendintr()  # in case the subprocess was not ended by the test
    p.wait()  # without wait() the coverage info never arrives


def test_list(example_app):
    example_app.expect(textwrap.dedent("""\
        ? What do you want to do?  (Use arrow keys)
         ❯ Order a pizza
           Make a reservation
           ---------------
           Ask for opening hours
           - Contact support (Unavailable at this time)
           Talk to the receptionist"""))
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? What do you want to do?  Order a pizza
        ? What size do you need?  (Use arrow keys)
         ❯ Jumbo
           Large
           Standard
           Medium
           Small
           Micro"""))
    example_app.write(keys.ENTER)
    # the following line is not necessary but "shows" how this works...
    example_app.expect(textwrap.dedent("""\
        ? What size do you need?  Jumbo
        {
            "size": "jumbo", 
            "theme": "Order a pizza"
        }
        
        """))
