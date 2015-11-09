#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
from protocols import UDP, ECPProtocols
from utils import Logger, handle_args
log = Logger(debug=settings.DEBUG_ECP)

if __name__ == "__main__":
    log.debug("Starting ECP server...")


    # handling argument
    # format of command is ./ecp [-p ECPport]
    # only (size) 3 arguments is alloweds
    args = handle_args(sys.argv, allowed_arguments=3, error_msg='./ecp [-p ECPport]')

    ECPname = settings.DEFAULT_ECPname
    ECPport = args.get('-p', settings.DEFAULT_ECPport)

    log.debug("Using ECPname = {}, ECPport = {}.".format(ECPname, ECPport))

    # running server
    udp = UDP(ECPname, ECPport)
    udp.run()

