#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import settings
from utils import Logger, handle_args
from protocols import TCP

log = Logger(debug=settings.DEBUG)

if __name__ == "__main__":
    log.debug("Starting TES server...")

    # handling arguments
    args = handle_args(sys.argv, allowed_arguments=1)
    TESport = args.get('-p', settings.DEFAULT_TESport)

    log.debug("Using TESport = {}".format(TESport))

    # running server
    tcp = TCP(settings.DEFAULT_TESname, TESport)
    tcp.run()
