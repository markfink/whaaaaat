# -*- coding: utf-8 -*-

from .helpers import remove_ansi_escape_sequences


def test_remove_ansi_escape_sequences():
    line = 'true\x1b[39;49;00m, \r\n    \x1b[34;01m"favorite"\x1b[39;49;00m: \x1b[33m"smoked bacon"\x1b[39;49;00m\r\n}\r\n\r\n'
    escaped_line = remove_ansi_escape_sequences(line)
    assert escaped_line == 'true,\n    "favorite": "smoked bacon"\n}\n\n'
