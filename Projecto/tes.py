#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
from protocols import TCP, TESProtocols
from utils import Logger, handle_args
log = Logger(debug=settings.DEBUG_TES)

if __name__ == "__main__":
    log.debug("Starting TES server...")

    # handling argument
    # format of command is ./tes [-p TESport] [-n ECPname] [-e ECPport],
    # only (size) 3 arguments is alloweds
    args = handle_args(sys.argv, allowed_arguments=7, error_msg='./tes [-p TESport] [-n ECPname] [-e ECPport]')
    TESport = args.get('-p', settings.DEFAULT_TESport)
    ECPname = args.get('-n', settings.DEFAULT_ECPname)
    ECPport = args.get('-e', settings.DEFAULT_ECPport)

    log.debug("Using TESport = {}, ECPname = {}, ECPport = {}.".format(TESport, ECPname, ECPport))

    # running server
    tcp = TCP(settings.DEFAULT_TESname, TESport)
    tcp.run(handle_data=TESProtocols(ECPname, ECPport))
