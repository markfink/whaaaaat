# -*- coding: utf-8 -*-
"""
Common test functionality
"""
import os
import sys
import regex
import codecs

from ptyprocess import PtyProcess

from prompt_toolkit.eventloop.posix import PosixEventLoop
from prompt_toolkit.input import PipeInput
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.output import DummyOutput

from inquirer import style_from_dict, Token
from inquirer import prompts


# http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/?in=user-97991
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

        # use Bunch to create group of variables:
        # cf = Bunch(datum=y, squared=y*y, coord=x)


keys = Bunch(
    DOWN='\x1b[B',
    UP='\x1b[A',
    LEFT='\x1b[D',
    RIGHT='\x1b[C',
    ENTER='\x0a',  # ControlJ  (Identical to '\n')
    ESCAPE='\x1b',
    CONTROLC='\x03',
    BACK='\x7f')


style = style_from_dict({
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


def feed_app_with_input(type, message, text, **kwargs):
    """
    Create a CommandLineInterface, feed it with the given user input and return
    the CLI object.

    This returns a (result, CLI) tuple.
    note: this only works if you import your prompt and then this function!!
    """
    # If the given text doesn't end with a newline, the interface won't finish.
    assert text.endswith('\n')

    application = getattr(prompts, type).question(message, **kwargs)

    loop = PosixEventLoop()
    try:
        inp = PipeInput()
        inp.send_text(text)
        cli = CommandLineInterface(
            application=application,
            eventloop=loop,
            input=inp,
            output=DummyOutput())
        result = cli.run()
        return result, cli
    finally:
        loop.close()
        inp.close()


def remove_ansi_escape_sequences(text):
    # http://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    # also clean up the line endings
    return regex.sub(r'(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]|\ *\r', '', text)


# helper for running sut as subprocess within pty
# does two things
# * test app running in pty in subprocess
# * get test coverage from subprocess

# docu:
# http://blog.fizyk.net.pl/blog/gathering-tests-coverage-for-subprocesses-in-python.html


PY3 = sys.version_info[0] >= 3


class SimplePty(PtyProcess):
    """Simple wrapper around a process running in a pseudoterminal.

    This class exposes a similar interface to :class:`PtyProcess`, but its read
    methods return unicode, and its :meth:`write` accepts unicode.
    """
    if PY3:
        string_type = str
    else:
        string_type = unicode   # analysis:ignore

    def __init__(self, pid, fd, encoding='utf-8', codec_errors='strict'):
        super(SimplePty, self).__init__(pid, fd)
        self.encoding = encoding
        self.codec_errors = codec_errors
        self.decoder = codecs.getincrementaldecoder(encoding)(errors=codec_errors)

    def read(self, size=1024):
        """Read at most ``size`` bytes from the pty, return them as unicode.

        Can block if there is nothing to read. Raises :exc:`EOFError` if the
        terminal was closed.

        The size argument still refers to bytes, not unicode code points.
        """
        b = super(SimplePty, self).read(size)
        if self.skip_cr:
            b = b.replace('\r', '')
        if self.skip_ansi:
            b = remove_ansi_escape_sequences(b)
        return self.decoder.decode(b, final=False)

    def readline(self):
        """Read one line from the pseudoterminal, and return it as unicode.

        Can block if there is nothing to read. Raises :exc:`EOFError` if the
        terminal was closed.
        note: this is a specialized version that does not have \r\n at the end
        """
        b = super(SimplePty, self).readline().strip()
        if self.skip_ansi:
            b = remove_ansi_escape_sequences(b)
        return self.decoder.decode(b, final=False)

    def write(self, s, skip_echo=True):
        """Write the unicode string ``s`` to the pseudoterminal.
        note: this is special since it does consume the echo from stdout already.
        This intends to make tests a little less verbose.

        Returns the number of bytes written.
        """
        b = s.encode(self.encoding)
        count = super(SimplePty, self).write(b)
        if skip_echo:
            assert self.read() == b
        return count

    def writeline(self, s):
        """Syntactic sugar to add a '\n' at the end of the .

        Returns the number of bytes written.
        """
        if not s.endswith('\n'):
            s += '\n'
        b = s.encode(self.encoding)
        return self.write(b)

    @classmethod
    def spawn(
            cls, argv, cwd=None, env=None, echo=True, preexec_fn=None,
            dimensions=(24, 80), skip_cr=True, skip_ansi=True):
        if env is None:
            env = os.environ
        inst = super(SimplePty, cls).spawn(argv, cwd, env, echo, preexec_fn,
                                           dimensions)
        inst.skip_cr = skip_cr
        inst.skip_ansi = skip_ansi
        return inst

    def __eq__(self, other):
        """Syntactic sugar to avoid calling read() all the time"""
        if isinstance(other, basestring):
            return self.read() == other
        return False

    '''
    # from pexpect/pty_spawn in case we need the nonblocking/timeout read
    # or see expect/expect.py expect_loop
    def read_nonblocking(self, size=1, timeout=-1):
        """This reads at most size characters from the child application. It
        includes a timeout. If the read does not complete within the timeout
        period then a TIMEOUT exception is raised. If the end of file is read
        then an EOF exception will be raised.  If a logfile is specified, a
        copy is written to that log.

        If timeout is None then the read may block indefinitely.
        If timeout is -1 then the self.timeout value is used. If timeout is 0
        then the child is polled and if there is no data immediately ready
        then this will raise a TIMEOUT exception.

        The timeout refers only to the amount of time to read at least one
        character. This is not affected by the 'size' parameter, so if you call
        read_nonblocking(size=100, timeout=30) and only one character is
        available right away then one character will be returned immediately.
        It will not wait for 30 seconds for another 99 characters to come in.

        This is a wrapper around os.read(). It uses select.select() to
        implement the timeout. """

        if self.closed:
            raise ValueError('I/O operation on closed file.')

        if timeout == -1:
            timeout = self.timeout

        # Note that some systems such as Solaris do not give an EOF when
        # the child dies. In fact, you can still try to read
        # from the child_fd -- it will block forever or until TIMEOUT.
        # For this case, I test isalive() before doing any reading.
        # If isalive() is false, then I pretend that this is the same as EOF.
        if not self.isalive():
            # timeout of 0 means "poll"
            r, w, e = select_ignore_interrupts([self.child_fd], [], [], 0)
            if not r:
                self.flag_eof = True
                raise EOF('End Of File (EOF). Braindead platform.')
        elif self.__irix_hack:
            # Irix takes a long time before it realizes a child was terminated.
            # FIXME So does this mean Irix systems are forced to always have
            # FIXME a 2 second delay when calling read_nonblocking? That sucks.
            r, w, e = select_ignore_interrupts([self.child_fd], [], [], 2)
            if not r and not self.isalive():
                self.flag_eof = True
                raise EOF('End Of File (EOF). Slow platform.')

        r, w, e = select_ignore_interrupts([self.child_fd], [], [], timeout)

        if not r:
            if not self.isalive():
                # Some platforms, such as Irix, will claim that their
                # processes are alive; timeout on the select; and
                # then finally admit that they are not alive.
                self.flag_eof = True
                raise EOF('End of File (EOF). Very slow platform.')
            else:
                raise TIMEOUT('Timeout exceeded.')

        if self.child_fd in r:
            return super(spawn, self).read_nonblocking(size)

        raise ExceptionPexpect('Reached an unexpected state.')  # pragma: no cover
    '''
