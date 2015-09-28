#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from utils import Logger, handle_args
from protocols import TCP
log = Logger(debug=True)

DEFAULT_TESname = 'localhost'
# Default port of the TES server
DEFAULT_TESport = 59000


if __name__ == "__main__":
    log.debug("Starting TES server...")

    # handling arguments
    args = handle_args(sys.argv)
    TESport = args.get('-p', DEFAULT_TESport)

    log.debug("Using TESport = {}".format(TESport))

    tcp = TCP(DEFAULT_TESname, TESport)
    tcp.run()
    # forever
    #while(True):
        # waits for client input:
        #input_data = raw_input()

