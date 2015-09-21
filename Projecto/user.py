#!/usr/bin/python
# -*- coding: utf-8 -*-

# import utils.global_utils; utils.global_utils.read_env() ## read .env vars
# from utils.global_utils import ArgOrigin, error_nc, error, logger, handle_args
# from utils.socket_utils import udp_client_request, tcp_client_request, tcp_client_request_send_and_receive, tcp_client_request_open, tcp_client_request_close

import sys, os

# Default port of the ECP server
ECP_PORT = 58054
# Default name of the ECP server
ECP_NAME = 'lima'

if __name__ == "__main__":
    print("Starting client...")

    ## handling arguments
    args = sys.argv
    if len(args) > 5:
        print("Error: too many arguments. Please use form ./user [-n ECPname] [-p ECPport]")
        sys.exit()

    if "-n" in args:
        ECPname = args[2]
    else:
        ECPname = ECP_NAME

    if "-p" in args:
        ECPport = args[4]
    else:
        ECPport = ECP_PORT

    print("Using ECPname = {} and ECPport = {}".format(ECPname, ECPport))


    ## for the while loop
    while(True):

        # 4 commands
        # list - chama o ECP com UDP as protocol. pede a lista de topicos
        # request - Topic NUm (Tnn) por TCP chama o TES respectivo
        # submit <answers_sequece> - TCP Tes resposta
        # exit - exit

        input_data = raw_input("")

        if 'list' in input_data:
            print("listing stuf > {}".format(input_data))
        elif 'request' in input_data:
            print("requesting stuf > {}".format(input_data))
        elif 'submit' in input_data:
            print("stuf tem dois éfes > {}".format(input_data))
        elif 'exit' in input_data:
            break

    print("Exiting client...")
