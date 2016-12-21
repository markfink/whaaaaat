# -*- coding: utf-8 -*-
import textwrap

import pytest

from .helpers import remove_ansi_escape_sequences, SimplePty


def test_remove_ansi_escape_sequences():
    line = 'true\x1b[39;49;00m, \r\n    \x1b[34;01m"favorite"\x1b[39;49;00m: \x1b[33m"smoked bacon"\x1b[39;49;00m\r\n}\r\n\r\n'
    escaped_line = remove_ansi_escape_sequences(line)
    assert escaped_line == 'true,\n    "favorite": "smoked bacon"\n}\n\n'


@pytest.fixture
def example_app():
    # users are expected to sendintr() to subprocess if it does not terminate itself
    p = SimplePty.spawn(['python', 'tests/example_app.py'])
    yield p
    p.wait()  # without the wait the coverage info never arrives


def test_example_app(example_app):
    # test the helper class plus demonstrate how to use it...
    assert example_app == textwrap.dedent("""\
        hi, there!
        let's get to know each other better...
        Please enter your name: """)
    example_app.writeline('Stuart')
    assert example_app.readline() == 'Hi Stuart, have a nice day!'


def test_example_app_no_match(example_app):
    # test the helper class plus demonstrate how to use it...
    assert not example_app == 'babadam'
    example_app.writeline('Stuart')
    assert example_app.readline() == 'Hi Stuart, have a nice day!'


def test_example_app_regex(example_app):
    assert example_app.equals_regex('hi, there!\n.*\nPlease enter your name: ')
    example_app.writeline('Stuart')
    assert example_app.readline() == 'Hi Stuart, have a nice day!'


def test_example_app_regex_no_match(example_app):
    assert not example_app.equals_regex('babadam')
    # note:
    # here we demonstrate how to exit the subprocess in case it is not expected
    # to close
    example_app.sendintr()

