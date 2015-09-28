# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys

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

def handle_args(arguments, allowed_arguments=2):
    '''
    makes all verification to user arguments and returns
    a dictionary with all args
    '''
    # format of command is ./user [-n ECPname] [-p ECPport]
    # only (size) 5 arguments is allowed
    log = Logger()

    if len(arguments) > (allowed_arguments * 2) + 1:
        log.error("Too many arguments.\nUse ./user [-n ECPname] [-p ECPport]")
        sys.exit()

    dictionary = {}
    allowed_args = ['-n', '-p']

    for arg in allowed_args:
        if arg in arguments:
            # get current element's index on array
            index_of = arguments.index(arg)
            # get value from that index + 1
            dictionary[arg] = arguments[index_of + 1]

    return dictionary

