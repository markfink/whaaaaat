# -*- coding: utf-8 -*-

from __future__ import print_function
import prompts
from prompts import list, confirm
from prompt_toolkit.shortcuts import run_application

from . import PromptParameterException


def prompt(questions, answers=None, **kwargs):
    answers = answers or {}

    patch_stdout = kwargs.pop('patch_stdout', False)
    return_asyncio_coroutine = kwargs.pop('return_asyncio_coroutine', False)
    true_color = kwargs.pop('true_color', False)
    refresh_interval = kwargs.pop('refresh_interval', 0)
    eventloop = kwargs.pop('eventloop', None)

    for question in questions:
        # import the question
        if not 'type' in question:
            raise PromptParameterException('type')
        if not 'name' in question:
            raise PromptParameterException('name')
        if not 'message' in question:
            raise PromptParameterException('message')
        try:
            kwargs.update(question)
            type = kwargs.pop('type')
            name = kwargs.pop('name')
            message = kwargs.pop('message')
            application = getattr(prompts, type).question(name, message,
                                                          **kwargs)

            answer = run_application(
                application,
                patch_stdout=patch_stdout,
                return_asyncio_coroutine=return_asyncio_coroutine,
                true_color=true_color,
                refresh_interval=refresh_interval,
                eventloop=eventloop)
            if answer is not None:
                answers[name] = answer
        except AttributeError as e:
            print(e)
            raise ValueError('No question type \'%s\'' % type)
        except KeyboardInterrupt:
            print('')
            print('Cancelled by user')
            print('')
            return {}
    return answers


# TODO:
# Bottom Bar - inquirer.ui.BottomBar
