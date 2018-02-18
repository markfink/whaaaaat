# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import os
import sys
import time
import threading
import textwrap
from six import exec_, PY2

#from prompt_toolkit.shortcuts import run_application

from . import PromptParameterException, prompts
from .prompts import list, confirm, input, password, checkbox, rawlist, expand


from prompt_toolkit.document import Document
from prompt_toolkit.application import Application
from prompt_toolkit.utils import is_conemu_ansi, is_windows
import prompt_toolkit.eventloop
#from prompt_toolkit.filters import to_simple_filter
from prompt_toolkit.filters.base  import Always, Never

'''
# from master:
def to_simple_filter(bool_or_filter):
    """
    Accept both booleans and CLIFilters as input and
    turn it into a SimpleFilter.
    """
    _always = Always()
    _never = Never()

    if not isinstance(bool_or_filter, (bool, SimpleFilter)):
        raise TypeError('Expecting a bool or a SimpleFilter instance. Got %r' % bool_or_filter)

    return {
        True: _always,
        False: _never,
    }.get(bool_or_filter, bool_or_filter)


if is_windows():
    from prompt_toolkit.output.win32_output import Win32Output
    from prompt_toolkit.output.conemu_output import ConEmuOutput
else:
    from prompt_toolkit.output.vt100 import Vt100_Output


def create_eventloop(inputhook=None, recognize_win32_paste=True):
    """
    Create and return an
    :class:`~prompt_toolkit.eventloop.base.EventLoop` instance for a
    :class:`~prompt_toolkit.interface.CommandLineInterface`.
    """
    if is_windows():
        from prompt_toolkit.eventloop.win32 import Win32EventLoop as Loop
        return Loop(inputhook=inputhook, recognize_paste=recognize_win32_paste)
    else:
        from prompt_toolkit.eventloop.posix import PosixEventLoop as Loop
        return Loop(inputhook=inputhook)


def create_output(stdout=None, true_color=False, ansi_colors_only=None):
    """
    Return an :class:`~prompt_toolkit.output.Output` instance for the command
    line.
    :param true_color: When True, use 24bit colors instead of 256 colors.
        (`bool` or :class:`~prompt_toolkit.filters.SimpleFilter`.)
    :param ansi_colors_only: When True, restrict to 16 ANSI colors only.
        (`bool` or :class:`~prompt_toolkit.filters.SimpleFilter`.)
    """
    stdout = stdout or sys.__stdout__
    true_color = to_simple_filter(true_color)

    if is_windows():
        if is_conemu_ansi():
            return ConEmuOutput(stdout)
        else:
            return Win32Output(stdout)
    else:
        term = os.environ.get('TERM', '')
        if PY2:
            term = term.decode('utf-8')

        return Vt100_Output.from_pty(
            stdout, true_color=true_color,
            ansi_colors_only=ansi_colors_only, term=term)


def create_asyncio_eventloop(loop=None):
    """
    Returns an asyncio :class:`~prompt_toolkit.eventloop.EventLoop` instance
    for usage in a :class:`~prompt_toolkit.interface.CommandLineInterface`. It
    is a wrapper around an asyncio loop.
    :param loop: The asyncio eventloop (or `None` if the default asyncioloop
                 should be used.)
    """
    # Inline import, to make sure the rest doesn't break on Python 2. (Where
    # asyncio is not available.)
    if is_windows():
        from prompt_toolkit.eventloop.asyncio_win32 import Win32AsyncioEventLoop as AsyncioEventLoop
    else:
        from prompt_toolkit.eventloop.asyncio_posix import PosixAsyncioEventLoop as AsyncioEventLoop

    return AsyncioEventLoop(loop)


def run_application(
        application, patch_stdout=False, return_asyncio_coroutine=False,
        true_color=False, refresh_interval=0, eventloop=None):
    """
    Run a prompt toolkit application.
    :param patch_stdout: Replace ``sys.stdout`` by a proxy that ensures that
            print statements from other threads won't destroy the prompt. (They
            will be printed above the prompt instead.)
    :param return_asyncio_coroutine: When True, return a asyncio coroutine. (Python >3.3)
    :param true_color: When True, use 24bit colors instead of 256 colors.
    :param refresh_interval: (number; in seconds) When given, refresh the UI
        every so many seconds.
    """
    assert isinstance(application, Application)

    if return_asyncio_coroutine:
        eventloop = create_asyncio_eventloop()
    else:
        eventloop = eventloop or create_eventloop()

    # Create CommandLineInterface.
    cli = CommandLineInterface(
        application=application,
        eventloop=eventloop,
        output=create_output(true_color=true_color))

    # Set up refresh interval.
    if refresh_interval:
        done = [False]
        def start_refresh_loop(cli):
            def run():
                while not done[0]:
                    time.sleep(refresh_interval)
                    cli.request_redraw()
            t = threading.Thread(target=run)
            t.daemon = True
            t.start()

        def stop_refresh_loop(cli):
            done[0] = True

        cli.on_start += start_refresh_loop
        cli.on_stop += stop_refresh_loop

    # Replace stdout.
    patch_context = cli.patch_stdout_context(raw=True) if patch_stdout else DummyContext()

    # Read input and return it.
    if return_asyncio_coroutine:
        # Create an asyncio coroutine and call it.
        exec_context = {'patch_context': patch_context, 'cli': cli,
                        'Document': Document}
        exec_(textwrap.dedent('''
'''
        def prompt_coro():
            # Inline import, because it slows down startup when asyncio is not
            # needed.
            import asyncio
            @asyncio.coroutine
            def run():
                with patch_context:
                    result = yield from cli.run_async()
                if isinstance(result, Document):  # Backwards-compatibility.
                    return result.text
                return result
            return run()
'''
'''), exec_context)

        return exec_context['prompt_coro']()
    else:
        try:
            with patch_context:
                result = cli.run()

            if isinstance(result, Document):  # Backwards-compatibility.
                return result.text
            return result
        finally:
            eventloop.close()
'''


def prompt(questions, answers=None, **kwargs):
    if isinstance(questions, dict):
        questions = [questions]
    answers = answers or {}

    # this functionality is obsolete:
    #patch_stdout = kwargs.pop('patch_stdout', False)
    #return_asyncio_coroutine = kwargs.pop('return_asyncio_coroutine', False)
    #true_color = kwargs.pop('true_color', False)
    #eventloop = kwargs.pop('eventloop', None)
    #refresh_interval = kwargs.pop('refresh_interval', 0)

    for question in questions:
        # import the question
        if not 'type' in question:
            raise PromptParameterException('type')
        if not 'name' in question:
            raise PromptParameterException('name')
        if not 'message' in question:
            raise PromptParameterException('message')
        try:
            _kwargs = {}
            _kwargs.update(kwargs)
            _kwargs.update(question)
            type = _kwargs.pop('type')
            name = _kwargs.pop('name')
            message = _kwargs.pop('message')
            when = _kwargs.pop('when', None)
            filter = _kwargs.pop('filter', None)
            if when:
                # at least a little sanity check!
                if callable(question['when']):
                    try:
                        if not question['when'](answers):
                            continue
                    except Exception as e:
                        raise ValueError(
                            'Problem in \'when\' check of %s question: %s' %
                            (name, e))
                else:
                    raise ValueError('\'when\' needs to be function that ' \
                                     'accepts a dict argument')
            if filter:
                # at least a little sanity check!
                if not callable(question['filter']):
                    raise ValueError('\'filter\' needs to be function that ' \
                                     'accepts an argument')

            if callable(question.get('default')):
                _kwargs['default'] = question['default'](answers)

            answer = getattr(prompts, type).question(message, **_kwargs)
            #answer = run_application(
            #    application,
            #    patch_stdout=patch_stdout,
            #    return_asyncio_coroutine=return_asyncio_coroutine,
            #    true_color=true_color,
            #    refresh_interval=refresh_interval,
            #    eventloop=eventloop)

            if answer is not None:
                if filter:
                    try:
                        answer = question['filter'](answer)
                    except Exception as e:
                        raise ValueError(
                            'Problem processing \'filter\' of %s question: %s' %
                            (name, e))
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
