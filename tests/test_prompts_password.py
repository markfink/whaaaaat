# -*- coding: utf-8 -*-
from whaaaaat.prompts import password  # this import is necessary!
from .helpers import feed_app_with_input, keys

# TODO tests from Inquirer.js


def test_basic_input():
    message = '? foo message'
    kwargs = {}
    text = 'MoinMoin' + keys.ENTER

    result, _ = feed_app_with_input('password', message, text, **kwargs)
    assert result == 'MoinMoin'


def test_delete_input():
    message = '? foo message'
    kwargs = {}
    text = 'MoinMoin' + 4*keys.BACK + keys.ENTER

    result, _ = feed_app_with_input('password', message, text, **kwargs)
    assert result == 'Moin'
