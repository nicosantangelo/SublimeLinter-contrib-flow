#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Nicolas Santangelo
# Copyright (c) 2014 Nicolas Santangelo
#
# License: MIT
#

"""This module exports the Flow plugin class."""

from SublimeLinter.lint import Linter, util


class Flow(Linter):

    """Provides an interface to flow."""

    syntax = ('javascript', 'javascriptnext')
    cmd = 'flow check'
    executable = 'flow'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.1.0'
    regex = r'''(?xi)
        # First line is the file, line, col and optional message
        ^.+:(?P<line>\d+):(?P<col>\d+),\d+:\s?(?P<message_title>\w*)\r?\n

        # Second line is the message
        ^(?P<message>.+)$
    '''
    multiline = True
    line_col_base = (1, 1)
    tempfile_suffix = None
    error_stream = util.STREAM_STDOUT
    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = r'\s*/[/*]'
    config_file = ('.flowconfig')

    #  TODO: Override def cmd(self): here to provide an executable path and --libs support using the Settings

    def split_match(self, match):
        """
        Return the components of the match.
        We override this to catch linter error messages and return more presise
        info used for highlighting.
        """
        # restore word regex to default each iteration
        self.word_re = None

        if match:
            message_title = match.group('message_title')
            message = match.group('message')

            # force line numbers to be at least 0
            # if not they appear at end of file
            line = max(int(match.group('line')) - 1, 0)
            col = int(match.group('col')) - 1
            error = None
            warning = None
            near = None

            if message_title:
                message = message_title + " " + message

            return match, line, col, error, warning, message, near

        return match, None, None, None, None, '', None

