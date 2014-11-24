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

import os
import re
from SublimeLinter.lint import Linter, util


class Flow(Linter):

    """Provides an interface to flow."""

    syntax = ('javascript', 'javascriptnext')
    cmd = 'flow check --show-all-errors'
    executable = 'flow'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.1.0'
    regex = r'''(?xi)
        # Warning location and optional title for the message
        /.+/(?P<file_name>.+):(?P<line>\d+):(?P<col>\d+),\d+:\s?(?P<message_title>.*)\r?\n

        # Main lint message
        (?P<message>.+)

        # Optional message, only extract the text, leave the path
        (\r?\n\s\s/.+:\s(?P<message_footer>.+))?
    '''
    multiline = True
    line_col_base = (1, 1)
    tempfile_suffix = None
    error_stream = util.STREAM_STDOUT
    selectors = {}
    word_re = None
    defaults = {
        # Allows the user to lint *all* files, regardless of whether they have the `/* @flow */` declaration at the top.
        'all': False,

        # Options for flow
        '--lib:,': ''
    }
    inline_settings = None
    inline_overrides = None
    comment_re = r'\s*/[/*]'
    config_file = ('.flowconfig')

    def cmd(self):
        """Return the command line to execute."""
        command = [self.executable_path, 'check', '--show-all-errors']

        if self.get_merged_settings()['all']:
            command.append('--all')

        return command

    def split_match(self, match):
        """
        Return the components of the match.
        We override this to catch linter error messages and return more presise
        info used for highlighting.
        """
        # restore word regex to default each iteration
        self.word_re = None
        if match:
            open_file_name = os.path.basename(self.view.file_name())
            linted_file_name = match.group('file_name')

            if linted_file_name == open_file_name:
                message_title = match.group('message_title')
                message = match.group('message')
                message_footer = match.group('message_footer') or ""

                # force line numbers to be at least 0
                # if not they appear at end of file
                line = max(int(match.group('line')) - 1, 0)
                col = int(match.group('col')) - 1
                error = None
                warning = None
                near = None

                if message_title:
                    message = message_title + " " + message + " " + message_footer

                return match, line, col, error, warning, message, near

        return match, None, None, None, None, '', None

