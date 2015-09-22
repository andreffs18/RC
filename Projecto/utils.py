# !/usr/bin/python
# -*- coding: utf-8 -*-


class Logger(object):
    '''
    Utils Logging
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


def handle_args(arguments):
    '''
    makes all verification to user arguments and returns
    a dictionary with all args
    '''
    # format of command is ./user [-n ECPname] [-p ECPport]
    # only (size) 5 arguments is allowed
    if len(arguments) > 5:
        log.error("Too many arguments.\nUse ./user [-n ECPname] [-p ECPport]")
        sys.exit()

    dictionary = {}
    # try to get name from arguments
    if "-n" in arguments:
        dictionary['-n'] = args[2]

    # try to get port from arguments
    if "-p" in arguments:
        dictionary['-p'] = args[4]

    return dictionary
