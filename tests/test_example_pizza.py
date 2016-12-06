# -*- coding: utf-8 -*-

import pytest
import pexpect


from .helpers import feed_app_with_input, keys


@pytest.fixture
def example_pizza():
    sut = pexpect.spawn('python examples/pizza.py')
    sut.expect('Hi, welcome to Python Pizza.*', timeout=1)
    yield sut


def test_select_first_choice(example_pizza):
    example_pizza.send(keys.ENTER)
    example_pizza.expect('.*What size do you need.*', timeout=1)
    example_pizza.send(keys.ENTER)
    example_pizza.expect('.*What size do you need.*', timeout=1)
    example_pizza.send(keys.ENTER)
    example_pizza.expect(
        '.*For a large pizza, you get a freebie.*(Use arrow keys)*', timeout=1)
    example_pizza.send(keys.ENTER)
    example_pizza.expect('.*Order receipt.*', timeout=1)
