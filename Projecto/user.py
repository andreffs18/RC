import utils.global_utils; utils.global_utils.read_env() ## read .env vars

import sys, os
from utils.global_utils import ArgOrigin, error_nc, error, logger, handle_args
from utils.socket_utils import udp_client_request, tcp_client_request, tcp_client_request_send_and_receive, tcp_client_request_open, tcp_client_request_close


if __name__ == "__main__":
    logger("Starting client...")
        
        ## handling arguments
        cshost, csport = handle_args(sys.argv, ArgOrigin.CLIENT)
        sshost, ssport = None, None
        
        ## for the while loop
        status = True
        while(status):
            ## input user arguments
            arg = raw_input("Select command: ").split(" ")
                
                if arg[0] == "list":
                    sshost, ssport = _list(cshost, csport)
                elif arg[0] == "retrieve":
                    try:
                        if ssport is None or sshost is None:
                            error_nc(__name__, "No Storage Server Found. Call \"list\" first.")
                                elif arg[1] == '' or arg[1].isspace():
                                    raise IndexError
                                else:
                                    _retrieve(arg[1], sshost, ssport)
                    except IndexError:
                        error_nc(__name__, "No filename.\nusage: retrieve <filename>")
                            
                            elif arg[0] == "upload":	
                                try:
                                if arg[1] == '' or arg[1].isspace():
                                    raise IndexError
                                _upload(arg[1], cshost, csport)
                                    except IndexError:
                                        error_nc(__name__, "No filename.\nusage: upload <filename>")
                                            
                                            elif arg[0] == "exit":
                                                status = not status
                                                    else:
                                                        error_nc(__name__, "Option Not Valid.")
                                                    
    logger("Exiting client...")
