# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import time
import textwrap

import pytest

from .helpers import keys, SimplePty


@pytest.fixture
def example_app():
    p = SimplePty.spawn(['python', 'examples/expand.py'])
    yield p
    # it takes some time to collect the coverage data
    # if the main process exits too early the coverage data is not available
    time.sleep(p.delayafterterminate)
    p.sendintr()  # in case the subprocess was not ended by the test
    p.wait()  # without wait() the coverage info never arrives


def test_without_expand(example_app):
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   (yAdxh)
        >> Overwrite this one and all next"""))
    example_app.write('x')
    example_app.expect(textwrap.dedent("""\
        
        Abot                          """))  # only registers changed chars :)
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   abort
        {
            "overwrite": "abort"
        }

        """))


def test_with_expand(example_app):
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   (yAdxh)
        >> Overwrite this one and all next"""))
    example_app.write('d')
    example_app.write('h')
    example_app.expect(
        "\n" +
        "  y) Ovewrite                    \n" +
        "  A) Overwrite this one and all next\n" +
        "  d) Show diff\n" +
        "   ---------------\n" +
        "  x) Abort\n" +
        "  h) Help, list all options\n" +
        "  Answer: d")
    example_app.write(keys.ENTER)
    example_app.expect(textwrap.dedent("""\
        ? Conflict on `file.js`:   diff
        {
            "overwrite": "diff"
        }

        """))
