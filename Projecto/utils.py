# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys

class Logger(object):
    '''
    Utils Logging
    has 4 variables that controls if the log goes to the output(screen)
    _error, _debug, _warning and _info
    default:  all loggers are enable except debug, which is False

    to enable debug log
    > log = Logger(debug=True)
    '''
    def __init__(self, debug=False, info=True, error=True, warning=True):
        self._error = error
        self._debug = debug
        self._warning = warning
        self._info = info

    def error(self, msg):
        if self._error:
            print("[ERROR]: {}".format(msg))

    def debug(self, msg):
        if self._debug:
            print("[DEBUG]: {}".format(msg))

    def info(self, msg):
        if self._info:
            print("[INFO]: {}".format(msg))

    def warning(self, msg):
        if self._warning:
            print("[WARNING]: {}".format(msg))

def handle_args(arguments, error_msg=None, allowed_arguments=2):
    '''
    makes all verification to user arguments and returns
    a dictionary with all args
    '''
    log = Logger()
    if len(arguments) > allowed_arguments:

        if error_msg:
            error_msg = "Use {}".format(error_msg)

        log.error("Too many arguments.\n{}.".format(error_msg))
        sys.exit()

    dictionary = {}
    allowed_args = ['-n', '-p', '-e']

    try:
        for arg in allowed_args:
            if arg in arguments:
                # get current element's index on array
                index_of = arguments.index(arg)
                # get value from that index + 1
                dictionary[arg] = arguments[index_of + 1]
    except IndexError:
        log.error("Too few arguments.\n{}.".format(error_msg))
        sys.exit()

    return dictionary
