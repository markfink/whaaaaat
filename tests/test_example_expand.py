# -*- coding: utf-8 -*-
import textwrap

import pytest
import pexpect
#import regex


from .helpers import feed_app_with_input, keys
#from .helpers import json_regex
from .helpers import remove_ansi_escape_sequences

@pytest.fixture
def example_expand():
    sut = pexpect.spawn('python examples/expand.py')
    #sut.expect('.*Do you like bacon.*\r\n', timeout=1)
    #sut.expect('.*bacon.*', timeout=2)
    yield sut


def test_without_expand(example_expand):
    example_expand.expect('.*Conflict on.*', timeout=1)
    example_expand.send('x')
    example_expand.expect('.*Abort.*', timeout=1)
    example_expand.send(keys.ENTER)
    # we want to do our own matching so we read till EOF (process stopped)
    example_expand.expect(pexpect.EOF)
    actual = remove_ansi_escape_sequences(example_expand.before)
    assert actual == textwrap.dedent("""\
        ? Conflict on `file.js`:   abort
        {
            "overwrite": "abort"
        }

        """)

