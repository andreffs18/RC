#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, socket
from protocols import UDP
from utils import Logger, handle_args_ecp
log = Logger(debug=True)

# Default port of the ECP server
DEFAULT_ECPport = 58054

DEFAULT_ECPname = 'localhost'





if __name__ == "__main__":
    log.debug("Starting Central ECP server...")

    # handling arguments
    args = handle_args_ecp(sys.argv)

    ECPport = args.get('-p', DEFAULT_ECPport)

    log.debug("Iniciou {}".format(ECPport))
    udp = UDP(DEFAULT_ECPname, DEFAULT_ECPport)
    udp.run()
    
