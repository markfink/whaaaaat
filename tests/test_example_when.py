# -*- coding: utf-8 -*-
import textwrap

import pytest
import pexpect
#import regex


from .helpers import feed_app_with_input, keys
#from .helpers import json_regex
from .helpers import remove_ansi_escape_sequences

@pytest.fixture
def example_when():
    sut = pexpect.spawn('python examples/when.py')
    #sut.expect('.*Do you like bacon.*\r\n', timeout=1)
    #sut.expect('.*bacon.*', timeout=2)
    yield sut


def test_like_bacon(example_when):
    example_when.send(keys.ENTER)
    example_when.expect('.*Bacon lover, what is your favorite type of bacon.*', timeout=1)
    example_when.send('smoked bacon')
    example_when.expect('smoked bacon')
    example_when.send(keys.ENTER)
    # we want to do our own matching so we read till EOF (process stopped)
    example_when.expect(pexpect.EOF)
    actual = remove_ansi_escape_sequences(example_when.before)
    assert actual == textwrap.dedent("""\
        ? Bacon lover, what is your favorite type of bacon? smoked bacon
        {
            "bacon": true,
            "favorite": "smoked bacon"
        }

        """)


'''
def test_like_pizza(example_when):
    example_when.expect('.*', timeout=1)
    example_when.send('n')
    example_when.send('Y')
    example_when.expect('.*What is your favorite type of pizza.*',
                        timeout=1)
    example_when.send('Toscana')
    example_when.expect('Toscana')
    example_when.send(keys.ENTER)
    # we want to do our own matching so we read till EOF (process stopped)
    example_when.expect(pexpect.EOF)
    actual = remove_ansi_escape_sequences(example_when.before)
    assert actual == textwrap.dedent("""\
        ? Whew! What is your favorite type of pizza? Toscana
        {
            "bacon": false,
            "favorite": "Toscana",
            "pizza": true
        }

        """)
'''
