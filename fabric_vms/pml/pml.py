#!/bin/env/python
# -*- coding: UTF-8 -*-
from __future__ import absolute_import

import cStringIO
import random
import string

from fabric.api import env, hide, put, settings, show
from ..openvms import run


__all__ = (
           'run_pml_commands',
           'run_pml_file'
)


SEPARATOR = '\r\n'  # newline separator
env.setdefault('temp_dir', 'TCPIP$SSH_HOME')  # Default temporary file folder


def run_pml_commands(cmd_list):
    """
        Run a list of commands in XURA v5's PML interface
        cmd_list: either a string with a single-line command or a list of
                  strings to be executed serially
    """
    if not isinstance(cmd_list, list):
        cmd_list = [cmd_list]
    # Create a temporary file with the command followed by 'disconnect, exit'
    cmd_file = cStringIO.StringIO()
    # The output will be sent to a temporary file with a random name
    # Everything is done remotely so we can use SYS$SCRATCH instead of
    # env.temp_dir.
    out_file = 'SYS$SCRATCH:%s.DAT' % (
        ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                             string.digits)
                for _ in range(8))
    )
    cmd_file.write('CONNECT\n')
    cmd_file.write('DISABLE OPCOM\n')
    cmd_file.write('ENABLE OUTPUT /FILE=%s\n' % (out_file, ))
    cmd_file.write('CANCEL CLASS MD /ALARM=ALL\n')  # Discard log messages
    for cmd in cmd_list:
        cmd_file.write('%s\n' % (cmd, ))
    cmd_file.write('DISCONNECT\n')
    cmd_file.write('EXIT\n')  # Gracefully close the PML session
    # Runs the temporary file
    run_pml_file(cmd_file, out_file, show_running=False)
    # Close the file object
    cmd_file.close()


def run_pml_file(pml_file, out_file=None, show_running=True):
    """ Run PML script and returns on screen output """
    # pml_file may be a filename, or a file-like object

    # First we need to upload the PML file to the remote host
    pml_filename = \
        pml_file if isinstance(pml_file, str) \
        else '{}:fabric_temp.pml'.format(env.temp_dir)

    with hide('running'):
        put(pml_file, pml_filename)

    with settings(show('running') if show_running else hide('running')):
        # Then we run PML /INPUT=pml_file
        run('PML /OPCLASS=2 /QUEUE=FABRIC /RESPONSE_TIME=10 /PROMPT=">>> "'
            '/INPUT=%s' % (pml_filename, ))

    with hide('running'):
        # Type the contents of the output file
        run('TYPE %s' % (out_file, ))
        # Remove the temporary pml_file
        run('DELETE /NOLOG %s;*' % (pml_filename, ))
        # If any, delete the temporary output file
        if out_file:
            run('DELETE /NOLOG %s;*' % (out_file, ))
