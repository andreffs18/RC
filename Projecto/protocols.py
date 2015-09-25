# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime as date
from socket import *
from utils import Logger
log = Logger(debug=True)

# buffer size is equal to 1024mb*5 = 5mb
BUFFERSIZE = int(os.environ.get('BUFFERSIZE', 5120))


def get_correct_answers():
    # vai ao ficheiro buscar as respostas correctas
    return ["A", "C", "D", "D", "A"]


def _protocol_RQS(data):
    # expecting data -> SID QID V1 V2 V3 V4 V5
    # get sid and qid from data
    SID, QID = data[:2]
    # parse answers
    student_answers = data[2:]
    correct_answers = get_correct_answers()

    score = 0
    for s_ans, c_ans in zip(student_answers, correct_answers):
        if s_ans == c_ans:
            score += 20

    return "AQS {} {}".format(QID, score)
    # return "AQS QID 10000"
    # return '-1' # caso ja tenha passado o deadline
    # return "ERR"

def _protocol_RQT(data):
    # expecting data = SID
    SID = data[0]

    QID = "asgidyua89u13289e123"
    time = date.datetime.now().strftime("%d%b%Y_%H:%M:%S").upper()
    # QUAL A HORA QUE TEMOS DE DAR?
    size = len(quiz)
    quiz = "ficehiro bue giro com coisas aqui dentro#"

    return "AQT {} {} {} {}".format(QID, time, size, quiz)
    # return data = AQT QID time size data
    # return data ? ERR


def handle_server_data(data):
    # removes \n from string
    data = data[:-1]
    data = data.split(" ")

    protocol = data[0]
    data = data[1:]

    if protocol == "RQS":
        data = _protocol_RQS(data)
    elif protocol == "RQT":
        data = _protocol_RQT(data)
    else:
        data = "ERR"

    # put back the \n
    data += "\n"
    return data

class TCP(object):
    '''
    Class to wrap all TCP interactions between client and server
    '''
    def __init__(self, host, port, buffer_size=BUFFERSIZE, max_connections=1):
        self.host = host
        self.port = int(port)
        self.buffer_size = buffer_size
        self.max_connections = max_connections

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

    def run(self):
        '''
        TCP server
        '''
        # Todo comment this
        sock = socket(AF_INET, SOCK_STREAM)
        addr = (self.host, self.port)
        sock.bind(addr)
        sock.listen(self.max_connections)

        log.info("TCP Server is ready for connection on [{}:{}]".format(self.host, self.port))
        while True:
            connection, client_address = sock.accept()
            addr_ip, addr_port = client_address
            try:
                while True:
                    data = connection.recv(self.buffer_size)

                    if data:
                        log.debug("Request from {}:{} > \"{}\"".format(addr_ip, addr_port, data[:-1]))

                        data = handle_server_data(data)
                        connection.sendall(data)
                    else:
                        break
            finally:
                connection.close()


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
