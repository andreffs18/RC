# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import uuid
import settings
import datetime as date
from socket import *
from utils import Logger

log = Logger(debug=settings.DEBUG)

def _protocol_RQS(data):
    '''
    Following the submit instruction by the student, we send
    the score and save the data from this student for stats
    '''

    def _get_correct_answers(quiz_name):
        # TODO
        # go to quiz_name file and get correct answeres
        # quiz = open(quiz_name + "c_ans.pdf", "r")
        # data = quiz.read()
        # data = data.split(" ").rstrip()
        # return data
        return ["A", "C", "D", "D", "A"]

    def _get_deadline(quiz_name):
        # TODO
        # go to quiz_name file and get deadline
        # still don't know
        return datetime.datetime.strptime("09JAN2015_20:00:00", "%d%b%Y_%H:%M:%S")

    try:
        # get sid and qid from data
        SID, QID = data[:2]
        # student answers to compare with correct answers
        student_answers = data[2:]
        correct_answers = get_correct_answers(QID)

        # compute score
        score = 0
        for s_ans, c_ans in zip(student_answers, correct_answers):
            if s_ans == c_ans:
                score += 20

        # check deadline
        now = date.datetime.now() # TODO
        deadline = _get_deadline()
        if deadline < now:
            return "-1"

        return "AQS {} {}".format(QID, score)
    except:
        log.error("There was a problem submiting quiz to student.")
        return "ERR"


def _protocol_RQT(data):
    '''
    Student requests the TES to send one of the avaiable
    questionnaires on the selected topic. The student ID
    is provided.
    '''

    def _get_quiz(quiz_number):
        # open file and return data form that quiz_file
        # fich = open('quiz_number.pdf', "r")
        # return = fich.read()
        return "DUMMY TEXT FOR NOW"  # TODO FIX ME

    try:
        quiz_number = 1  # ??????
        # get student ID
        SID = data[0]
        # get quiz file data
        quiz = _get_quiz(quiz_number)
        # generate random QID for this transaction # TODO
        QID = uuid.uuid4().hex[:10] + SID
        # generate deadline which will be in an hour
        time = date.datetime.now().strftime("%d%b%Y_%H:%M:%S").upper() # TODO ^
        # size of the quiz
        size = len(quiz)
        return "AQT {} {} {} {}".format(QID, time, size, quiz)
    except:
        log.error("There was a problem returning quiz to student.")
        return "ERR"


def handle_tcp_server_data(data):
    # removes \n from string
    data = data[:-1]
    # split data into chunks
    data = data.split(" ")
    # get protocol and rest of the data
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
    def __init__(self, host, port, buffer_size=settings.BUFFERSIZE, max_connections=1):
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

    def request(self, data):
        '''
            makes tcp socket connection to host and port machine
            returns the raw response from the host machine
        '''
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.connect((self.host, self.port))
        try:
            log.debug("[TCP] Sending request to {}:{} > \"{}\"".format(self.host, self.port, self._remove_new_line(data)))
            # sock.send(data)
            sock.sendall(data)
            data = sock.recv(self.buffer_size)
            log.debug("[TCP] Got back > \"{}\"".format(self._remove_new_line(data)))
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
                        log.debug("Got request from {}:{} > \"{}\"".format(addr_ip, addr_port, data[:-1]))
                        data = handle_tcp_server_data(data)
                        log.debug("Sending back > \"{}\"".format(data[:-1]))
                        connection.sendall(data)
                    else:
                        break
            finally:
                connection.close()


class UDP(object):
    '''
    Class to wrap all UDP interactions between client and server
    '''
    def __init__(self, host, port, buffer_size=settings.BUFFERSIZE):
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
            log.debug("[UDP] Sending request to {}:{} > \"{}\"".format(self.host, self.port, self._remove_new_line(data)))
            sock.sendto(data, (self.host, self.port))
            data = sock.recv(self.buffer_size)
            log.debug("[UDP] Got back > \"{}\"".format(self._remove_new_line(data)))
        finally:
            sock.close()

        data = self._remove_new_line(data)
        return data
