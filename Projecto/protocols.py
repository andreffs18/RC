# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
from socket import *


# buffer size is equal to 1024mb*5 = 5mb
BUFFERSIZE = int(os.environ.get('BUFFERSIZE', 5120))


class TCP(object):
    '''
    Class to wrap all TCP interactions between client and server
    '''
    def __init__(self, host, port, buffer_size=BUFFERSIZE):
        self.host = host
        self.port = int(port)
        self.buffer_size = buffer_size

    def _remove_new_line(self, message):
        '''
        if exists, removes \n from the end of the message
        '''
        if message.endswith('\n'):
            return message[:-1]
        return message

    def fake_request(self, input, output):
        return output

    def request(self, data):
        '''
            makes tcp socket connection to host and port machine
            returns the raw response from the host machine
        '''
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        addr = (self.host, self.port)
        sock.connect(addr)
        try:
            sock.sendall(data)
            data = sock.recv(self.buffer_size)
        finally:
            sock.close()

        data = self._remove_new_line(data)
        return data


class UDP(object):
    '''
    Class to wrap all UDP interactions between client and server
    '''
    def __init__(self, host, port, buffer_size=BUFFERSIZE):
        self.host = host
        self.port = int(port)
        self.buffer_size = buffer_size

    def _remove_new_line(self, message):
        '''
        if exists, removes \n from the end of the message
        '''
        if message.endswith('\n'):
            return message[:-1]
        return message

    def fake_request(self, input, output):
        return output

    def request(self, data):
        '''
            makes udp socket connection to host and port machine
            returns the raw response from the host machine
        '''
        # TODO comment this code to know what is happenign
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        try:
            addr = (self.host, self.port)
            sock.sendto(data, addr)
            data = sock.recv(self.buffer_size)
        finally:
            sock.close()

        data = self._remove_new_line(data)
        return data
