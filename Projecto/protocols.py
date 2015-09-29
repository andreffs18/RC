# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import uuid
import settings
import datetime as date

from socket import *
from utils import Logger


log = Logger(debug=settings.DEBUG)


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
        tes = TESProtocols()
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
                        data = tes.dispatch(data)
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

    def run(self):
        '''
        UDP server
        '''
        ecp = ECPProtocols()
        try:
            s = socket(AF_INET, SOCK_DGRAM)
        except error, msg:
            log.error(msg)
            sys.exit()

        # Bind socket to local host and port
        try:
            s.bind((self.host, self.port))
        except error , msg:
            log.error(msg)
            sys.exit()

        log.info("UDP Server is ready for connection on [{}:{}]".format(self.host, self.port))
        #now keep talking with the client
        while True:
            # receive data from client (data, addr)
            data, addr = s.recvfrom(self.buffer_size)
            addr_ip, addr_port = addr
            if not data:
                break

            log.debug("Got request from {}:{} > \"{}\"".format(addr_ip, addr_port, self._remove_new_line(data)))
            data = ecp.dispatch(data)
            log.debug("Sending back > \"{}\"".format(self._remove_new_line(data)))

            s.sendto(data, addr)

        s.close()


class TESProtocols(object):
    '''
    Class to wrap all Endpoints for TES messages.
    '''

    def dispatch(self, data):
        '''
        this method parses and checks for with feature is the "data" requesting
        this works as a central hub, "switch", where it redirects to the correct
        method. as input is the data from the outside world, output is the
        handled data
        '''
        # removes \n from string
        data = data[:-1]
        # split data into chunks
        data = data.split(" ")
        # get protocol and rest of the data
        protocol = data[0]
        data = data[1:]

        if protocol == "RQS":
            data = _RQS(data)
        elif protocol == "RQT":
            data = _RQT(data)
        else:
            data = "ERR"

        # put back the \n
        data += "\n"
        return data

    def _RQS(self, data):
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
                log.info("There was a problem submiting quiz to student. Student submited quiz after deadline.")
                return "-1"

            log.info("Returning student obtain {} on the quiz {}.".format(score, QID))
            return "AQS {} {}".format(QID, score)
        except:
            log.error("There was a problem submiting quiz to student.")
            return "ERR"

    def _RQT(self, data):
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

            log.info("Quiz {} returned to student {}.".format(QID, SID))
            return "AQT {} {} {} {}".format(QID, time, size, quiz)
        except:
            log.error("There was a problem returning quiz to student.")
            return "ERR"


class ECPProtocols(object):
    '''
    Class to wrap all Endpoints for ECP messages.
    '''

    def dispatch(self, data):
        '''
        this method parses and checks for with feature is the "data" requesting
        this works as a central hub, "switch", where it redirects to the correct
        method. as input is the data from the outside world, output is the
        handled data
        '''
        # removes \n from string
        data = data[:-1]
        # split data into chunks
        data = data.split(" ")
        # get protocol and rest of the data
        protocol = data[0]
        data = data[1:]

        if protocol == "TQR":
            data = self._TQR(data)
        elif protocol == "TER":
            data = self._TER(data)
        else:
            data = "ERR"

        # put back the \n
        data += "\n"
        return data

    def __get_list_of_topics(self, details=False):
        '''
        '''
        with open(settings.TOPICS_FILE, 'r') as tfile:
            content = tfile.readlines()

        if not details:
            # returns array with topics name
            # ex: ['topic1', 'topic2', ...]
            return [t.split(" ")[0].rstrip() for t in content]
        else:
            # returns array with tuples of info about topics
            # ex: [('topic1', 'IP', 'PORT'), ('topic2', 'IP', 'PORT'), ...]
            return [tuple(map(lambda x: x.rstrip(), t.split(" "))) for t in content]

    def _TQR(self, data):
        '''
        '''
        try:
            topics = self.__get_list_of_topics()
            amount_of_topics = len(topics)

            if amount_of_topics == 0:
                log.error("There was a problem returning topics to student. There are no topics available at the moment.")
                return 'EOF'

            log.info("Returning list of {} topics.".format(amount_of_topics))
            return "AWT {} {}".format(amount_of_topics, " ".join(topics))
        except:
            log.error("There was a problem returning topics to student.")
            return "ERR"

    def _TER(self, data):
        '''
        '''
        try:
            topic_num = int(data[0])
            topics = self.__get_list_of_topics(details=True)

            if topic_num > len(topics):
                log.error("Topic number invalid. Topic number should not be bigger than the amount of topics.")
                return "EOF"

            if topic_num == 0:
                log.error("Topic number invalid. Topic number should not be zero.")
                return "EOF"

            topic = topics[topic_num - 1]
            _, TEShost, TESport = topic
            log.info("Returning TEShost = {} and TESport = {}.".format(TEShost, TESport))
            return "AWTES {} {}".format(TEShost, TESport)

        except ValueError:
            log.error("Topic number invalid. Should be a number and not \"{}\".".format(data))
            return "EOF"
        except:
            log.error("There was a problem returning quiz to student.")
            return "ERR"
