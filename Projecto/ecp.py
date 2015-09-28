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
	udp.start()
	#Create socket
    try:
    	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	log.debug("socket created")
    except socket.error, msg:
    	log.error(msg)
    	sys.exit()
	 
	# Bind socket to local host and port
	try:
	    s.bind(('localhost', ECPport))
	    log.debug("Bind completed")
	except socket.error , msg:
	    log.error(msg)
	    sys.exit()
	     
	 
	#now keep talking with the client
	while True:
	    # receive data from client (data, addr)
	    d = s.recvfrom(1024)
	    data = d[0]
	    addr = d[1]
	     
	    if not data: 
	        break
	     
	    reply = 'OK...' + data
	     
	    s.sendto(reply , addr)
	    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
	     
	s.close()