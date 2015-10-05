# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import uuid
import random
import settings
import datetime as date

from socket import *
from utils import Logger

# enable logs debug if DEBUG_TES or DEBUG_ECP is True
log = Logger(debug=settings.DEBUG_TES or settings.DEBUG_ECP)


class TCP(object):
    '''
    Class to wrap all TCP interactions between client and server
    '''
    def __init__(self, host, port, buffer_size=settings.BUFFERSIZE, max_connections=1):
        self.host = host
        self.buffer_size = buffer_size
        self.max_connections = max_connections
        try:
            self.port = int(port)
        except ValueError, msg:
            self.port = int(settings.DEFAULT_ECPport)
            log.error("{}. Using default port \"{}\".".format(msg, settings.DEFAULT_ECPport))

    def _remove_new_line(self, message):
        '''
        if exists, removes \n from the end of the message
        '''
        if message.endswith('\n'):
            return message[:-1]
        return message

    def _limit_amount(self, message):
        '''
        if data in msg is bigger than 60
        '''
        return message[:60]

    def request(self, data):
        '''
        makes tcp socket connection to host and port machine
        returns the raw response from the host machine
        '''
        # Create a new socket using the given address family, socket type and protocol number
        sock = socket(AF_INET, SOCK_STREAM)
        # Set the value of the given socket option (see the Unix manual page setsockopt(2)).
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        try:
            # Connect to a remote socket at address.
            sock.connect((self.host, self.port))
            # define timout to settings.TIMEOUT_DELAY
            sock.settimeout(settings.TIMEOUT_DELAY)
            log.debug("[TCP] Sending request to {}:{} > \"{}\".".format(self.host, self.port, self._remove_new_line(data)))
            # Send data to the socket.
            sock.sendall(data)
            # Receive data from the socket (max amount is the buffer size).
            data = sock.recv(self.buffer_size)
            # F#$% this. hack this way throught. it's late and we need to finish this
            # if by any means, the last char in received data is " " then we just
            # repeat the procces and increase the timeout 3 times.
            # otherwise we continue and don't repeat the process
            if data[-1] >= " ":
                sock.settimeout(settings.TIMEOUT_DELAY * 3)
                log.debug("Final char in data from request is " ".")
                old_data = ""
                while len(data) != len(old_data):
                    old_data = data
                    data += sock.recv(self.buffer_size)
                log.debug("Downloaded content size is {}.".format(len(data)))

            log.debug("[TCP] Got back > \"{}\".".format(self._remove_new_line(self._limit_amount(data))))
        # in case of timeout
        except timeout, msg:
            log.error("Request Timeout.")
            data = "ERR"
        # in case of error
        except error, msg:
            log.error("Something happen when trying to connect to {}:{}.".format(self.host, self.port))
            data = "ERR"
        finally:
            # Close socket connection
            sock.close()
        data = self._remove_new_line(data)
        return data

    def run(self, handle_data=None):
        '''
        TCP server. TES runs this server
        '''
        # Create a new socket using the given address family, socket type and protocol number
        sock = socket(AF_INET, SOCK_STREAM)
        try:
            addr = (self.host, self.port)
            # Bind the socket to address.
            sock.bind(addr)
            # Listen for connections made to the socket.
            sock.listen(self.max_connections)
        except error, msg:
            log.error("{}. Possible bad port definition or port already in user. Try again.".format(msg))
            sys.exit()

        log.info("TCP Server is ready for connection on [{}:{}].".format(self.host, self.port))
        while True:
            # Accept a connection.
            connection, client_address = sock.accept()
            # Get connection HostIP and HostPORT
            addr_ip, addr_port = client_address
            try:
                while True:
                    # Receive data from socket
                    data = connection.recv(self.buffer_size)
                    if data:
                        log.debug("Got request from {}:{} > \"{}\".".format(addr_ip, addr_port, self._remove_new_line(data)))

                        if not handle_data:
                            # Create instance of ECPProtocols to handle all data
                            handle_data = TESProtocols()

                        data = handle_data.dispatch(data)

                        log.debug("Sending back > \"{}\".".format(self._remove_new_line(self._limit_amount(data))))
                        # Send data to the socket.
                        connection.sendall(data)
                    else:
                        break
            finally:
                # Close socket connection
                connection.close()


class UDP(object):
    '''
    Class to wrap all UDP interactions between client and server
    '''
    def __init__(self, host, port, buffer_size=settings.BUFFERSIZE):
        self.host = host
        self.buffer_size = buffer_size
        try:
            self.port = int(port)
        except ValueError, msg:
            self.port = int(settings.DEFAULT_TESport)
            log.error("{}. Using default port \"{}\".".format(msg, settings.DEFAULT_TESport))

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
        # Create a new socket using the given address family, socket type and protocol number
        sock = socket(AF_INET, SOCK_DGRAM)
        # Set the value of the given socket option (see the Unix manual page setsockopt(2)).
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        # define timout to settings.TIMEOUT_DELAY
        sock.settimeout(settings.TIMEOUT_DELAY)
        try:
            log.debug("[UDP] Sending request to {}:{} > \"{}\".".format(self.host, self.port, self._remove_new_line(data)))
            # Send data to the socket.
            sock.sendto(data, (self.host, self.port))
            # Receive data from the socket (max amount is the buffer size).
            data = sock.recv(self.buffer_size)
            log.debug("[UDP] Got back > \"{}\".".format(self._remove_new_line(data)))
        # in case of timeout
        except timeout, msg:
            log.error("Request Timeout.")
            data = 'ERR'
        # in case of error
        except error, msg:
            log.error("Something happen when trying to connect to {}:{}.".format(self.host, self.port))
            data = "ERR"
        finally:
            # Close socket connection
            sock.close()
        data = self._remove_new_line(data)
        return data

    def run(self, handle_data=None):
        '''
        UDP server. ECP runs this server
        '''
        try:
            # Create a new socket using the given address family, socket type and protocol number
            s = socket(AF_INET, SOCK_DGRAM)
        except error, msg:
            log.error(msg)
            sys.exit()

        try:
            # Bind socket to local host and port
            s.bind((self.host, self.port))
        except error , msg:
            log.error(msg)
            sys.exit()

        log.info("UDP Server is ready for connection on [{}:{}].".format(self.host, self.port))
        # now keep talking with the client
        while True:
            # Receive data from client (data, addr)
            data, addr = s.recvfrom(self.buffer_size)
            # Get connection HostIP and HostPORT
            addr_ip, addr_port = addr
            if not data:
                break
            log.debug("Got request from {}:{} > \"{}\".".format(addr_ip, addr_port, self._remove_new_line(data)))

            if not handle_data:
                # Create instance of ECPProtocols to handle all data
                handle_data = ECPProtocols()
            data = handle_data.dispatch(data)

            log.debug("Sending back > \"{}\".".format(self._remove_new_line(data)))
            # Send data to the socket.
            s.sendto(data, addr)
        # Close socket connection
        s.close()


class TESProtocols(object):
    '''
    Class to wrap all Endpoints for TES messages.
    '''
    def __init__(self, host=settings.DEFAULT_ECPname, port=settings.DEFAULT_ECPport):
        '''
        inits udp instance (ECP SERVER)
        '''
        self.UDP = UDP(host, port)

    def dispatch(self, data):
        '''
        this method parses and checks for with feature is the "data" requesting
        this works as a central hub, "switch", where it redirects to the correct
        method. as input is the data from the outside world, output is the
        handled data
        '''
        # removes \n from string
        data = self.UDP._remove_new_line(data)
        # split data into chunks
        data = data.split(" ")
        # get protocol and rest of the data
        protocol = data[0]
        data = data[1:]
        # dispatch to correct method
        if protocol == "RQT":
            data = self._RQT(data)
        elif protocol == "RQS":
            data = self._RQS(data)
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
        def __get_fake_database():
            '''
            get all records of FAKE_DATABASE file
            '''
            with open(settings.FAKE_DATABASE, 'r') as db:
                content = db.readlines()
            return [tuple(map(lambda x: x.rstrip(), t.split(" "))) for t in content]

        def __db_find_quiz(quiz_name):
            '''
            get FAKE_DATABASE and search if there is a record with the "quiz_name"
            '''
            db = __get_fake_database()
            try:
                return [(qid, topic_name, deadline) for qid, topic_name, deadline in db if quiz_name == qid][0]
            except IndexError:
                log.error("No matches in fake db. Couldn't find entry with QID \"{}\".".format(quiz_name))
                return [("", "", "")]

        def __get_topic_name(quiz_name):
            _, topic_name, _ = __db_find_quiz(quiz_name)
            return "{}.txt".format(topic_name)

        def __get_correct_answers(quiz_name):
            '''
            go to quiz_name file and get correct answeres
            '''
            topic_name = __get_topic_name(quiz_name)
            filename = topic_name.split(".")[0] + "A.txt"
            try:
                with open(settings.QUIZ_PATH + "/{}".format(filename), 'r') as cquiz:
                    content = cquiz.readlines()
                return [line.rstrip() for line in content]
            except IOError, msg:
                log.error("There is no file with this name {}.".format(filename))
                return []

        def __get_deadline(quiz_name):
            '''
            go to quiz_name file and get deadline
            '''
            _, _, deadline = __db_find_quiz(quiz_name)
            return date.datetime.strptime(deadline, "%d%b%Y_%H:%M:%S")

        try:
            # get sid and qid from data
            SID, QID = data[:2]
            # check deadline
            now = date.datetime.now()
            deadline = __get_deadline(QID)
            if now > deadline:
                log.info("There was a problem submiting quiz to student. Student submited quiz after deadline.")
                return "-1"

            # student answers to compare with correct answers
            student_answers = data[2:]
            correct_answers = __get_correct_answers(QID)
            if len(correct_answers) == 0:
                log.info("There is no quiz with \"{}\" as QID belonging to \"{}\" student.".format(QID, SID))
                return "-2"

            # compute score
            score = 0
            for s_ans, c_ans in zip(student_answers, correct_answers):
                if s_ans == c_ans:
                    score += 20

            # send score to ECP server
            topic_name = __get_topic_name(QID)
            data = self.UDP.request("IQR {} {} {} {}\n".format(SID, QID, topic_name, score))
            # 2' handling response from request to ECP server
            # 2.1' error (ERR) - something unexpected happen
            if data.startswith('ERR'):
                log.debug("ERR occur from UDP request to ECP.")
                log.error("ERR - There was an error connecting to ECP server. Try again later.")
                return "ERR"
            # 2.2' return
            else:
                log.debug("No errors connecting to ECP with UDP Protocol.")
                data = data.split(' ')
                _QID = data[1]
                print("Updated stats on quiz {}".format(_QID))

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
        def __get_quiz_name():
            files = []
            for f in os.listdir(settings.QUIZ_PATH):
                if os.path.isfile(os.path.join(settings.QUIZ_PATH,f)) and '.txt' in f:
                    files.append(f)

            ## outrosfiches ['TnnQF1.txt', 'TnnQF1A.txt']
            ## remove all files tthat contains 'A'
            files = [f for f in files if 'A' not in f]
            quiz = random.choice(files)
            return quiz

        def __get_quiz(quiz_name):
            '''
            open file and return data form that quiz_file
            '''
            # quiz_name = 'TnnQF1.txt'
            with open(settings.QUIZ_PATH + "/{}".format(quiz_name), 'r') as tfile:
                content = tfile.read()
            return content

        def __get_data():
            '''
            returs data of file creation
            '''
            return date.datetime.now().strftime("%d%b%Y_%H:%M:%S").upper()

        def __get_deadline():
            '''
            just builds a datetime object and then parses it to the
            correct format DDMMMYYYY_HH:MM:SS
            '''
            deadline = date.datetime.now() + date.timedelta(0, settings.DEADLINE_DELTA)
            return deadline.strftime("%d%b%Y_%H:%M:%S").upper()

        try:
            # get student ID, and Tnn
            SID = data[0]
            # get quiz file data
            quiz_name = __get_quiz_name()
            quiz = __get_quiz(quiz_name)
            # generate random QID for this transaction
            QID = "{}_{}".format(SID, __get_data())
            # generate deadline which will be in an hour
            deadline = __get_deadline()
            # size of the quiz
            size = len(quiz)
            # save into db info about this quiz
            log.debug("Saving info into db.")
            with open(settings.FAKE_DATABASE, "a+") as db:
                db.write("{} {} {}\n".format(QID, quiz_name, deadline))

            log.info("Quiz {} returned to student {}.".format(QID, SID))
            return "AQT {} {} {} {}".format(QID, deadline, size, quiz)
        except:
            log.error("There was a problem returning quiz to student.")
            return "ERR"


class ECPProtocols(object):
    '''
    Class to wrap all Endpoints for ECP messages.
    '''
    def __init__(self, host=settings.DEFAULT_ECPname, port=settings.DEFAULT_ECPport):
        '''
        inits udp instance
        '''
        self.TCP = TCP(host, port)

    def dispatch(self, data):
        '''
        this method parses and checks for with feature is the "data" requesting
        this works as a central hub, "switch", where it redirects to the correct
        method. as input is the data from the outside world, output is the
        handled data
        '''
        # removes \n from string
        data = self.TCP._remove_new_line(data)
        # split data into chunks
        data = data.split(" ")
        # get protocol and rest of the data
        protocol = data[0]
        data = data[1:]
        # dispatch to correct method
        if protocol == "TQR":
            data = self._TQR(data)
        elif protocol == "TER":
            data = self._TER(data)
        elif protocol == "IQR":
            data = self._IQR(data)
        else:
            data = "ERR"
        # put back the \n
        data += "\n"
        return data

    def __get_list_of_topics(self, details=False):
        '''
        get TOPICS_FILE and return list of topics
        with details=True it returns list of topics with ip and port info
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
        Response to the list instruction from the student, we return the list of
        questionnaire topics available in the TES servers.
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
        Student request contains the identification of the desired questionnaire
        topic number (Tnn). We return TESip and TEShost for that topic
        '''
        try:
            topic_num = int(data[0])
            topics = self.__get_list_of_topics(details=True)
            if topic_num > len(topics):
                log.error("Topic number invalid. Topic number should not be bigger than the amount of topics.")
                return "EOF"
            if topic_num < 1 or topic_num > 99:
                log.error("Topic number invalid. Topic number should not be zero.")
                return "EOF"

            topic = topics[topic_num - 1]
            _, TEShost, TESport = topic
            log.info("Returning TEShost = \"{}\" and TESport = \"{}\".".format(TEShost, TESport))
            return "AWTES {} {}".format(TEShost, TESport)
        except ValueError:
            log.error("Topic number invalid. Should be a number and not \"{}\".".format(data))
            return "EOF"
        except:
            log.error("There was a problem returning quiz to student.")
            return "ERR"

    def _IQR(self, data):
        '''
        The TES informs the ECP that student SID answered questionnaire QID,
        on topic_name, and obtained the percentage score.
        '''
        try:
            SID, QID, topic_name, score = data
            # save this on STATS_FILE
            with open(settings.STATS_FILE, 'a+') as sfile:
                sfile.write("{} {} {} {}\n".format(SID, QID, topic_name, score))
            log.info("Saved info on student {} for quiz {}.".format(SID, QID))
            return "AWI {}".format(QID)
        except:
            log.error("There was a problem saving quiz infomation on ECP.")
            return "ERR"

