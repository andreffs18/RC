#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
from protocols import UDP, TCP
from utils import Logger, handle_args
log = Logger(debug=settings.DEBUG_USER)


def _list(ecpname, ecpport):
    # 1' send "TQR\n" to ECP server
    udp = UDP(ecpname, ecpport)
    message = 'TQR\n'
    data = udp.request(message)
    # data = udp.fake_request(message)

    # 2' handling response from request to ECP server
    # 2.1' error (EOF) - there is no topics available
    if data.startswith('EOF'):
        log.debug("EOF occur from UDP request to ECP.")
        log.error("EOF - No topic list available at the moment. Try again later.")
        return
    # 2.2' error (ERR) - something unexpected happen
    elif data.startswith('ERR'):
        log.debug("ERR occur from UDP request to ECP.")
        log.error("ERR - There was an error connecting to ECP server. Try again later.")
        return
    # 2.3' present list of topics
    else:
        log.debug("No errors connecting to ECP with UDP Protocol.")
        data = data.split(' ')
        amount_of_topics = int(data[1])
        topics = data[2:]
        # print on screen list of topics
        print("List of Topics from ECP Server:")
        for index, topic in enumerate(topics, 1):
            print("\t{} - {}").format(index, topic)
    log.debug("User command LIST complete.")


def _request(ecpname, ecpport, topic_num, SID):
    # 1' send "TER Tnn\n" to ECP server
    udp = UDP(ecpname, ecpport)
    message = 'TER {}\n'.format(topic_num)
    data = udp.request(message)

    TESip, TESport, QID = None, None, None
    # 2' handling response from request to ECP server
    # 2.1' error (EOF) - there is no topics available
    if data.startswith('EOF'):
        log.debug("EOF occur from UDP request to ECP.")
        log.error("EOF - Invalid topic number. Please try again with diferent topic number.")
    # 2.2' error (ERR) - something unexpected happen
    elif data.startswith('ERR'):
        log.debug("ERR occur from UDP request to ECP.")
        log.error("ERR - There was an error connecting to ECP server. Try again later.")
    # 2.3' returns message
    else:
        log.debug("No errors connecting to ECP with UDP Protocol.")
        data = data.split(" ")
        TESip, TESport = data[1:]

    if TESip and TESport:
        # in case everything went okay, we have a TES IP and PORT to connect to
        tcp = TCP(TESip, TESport)
        message = 'RQT {} {}\n'.format(SID, topic_num)
        data = tcp.request(message)

        # 2' handling response from request to TES server
        # 2.1' error (ERR) - something unexpected happen
        if data.startswith('ERR'):
            log.debug("ERR occur from TCP request to TES.")
            log.error("ERR - There was na error connection to TES server. Try again later.")
        # 2.2' returns message
        else:
            # validar bem esta popo se naot iver data beka beka
            log.debug("No errors connecting to TES with TCP Protocol.")
            data = data.split(" ")
            QID, deadline, size = data[1:4]
            data = " ".join(data[4:])
            filename = "{}.pdf".format(QID)
            print("Downloading and saving quiz \"{}\" with {} bytes.".format(filename, size))
            with open(filename, "w+") as qfile, open(settings.FAKE_DATABASE, "a+") as db:
                # save file to disk
                qfile.write(data)
                # save record in fake db
                db.write("{}\n".format(" ".join([QID, topic_num, deadline])))
            print("File saved. You have until {} to submit your answers.".format(deadline))
        log.debug("User command REQUEST complete.")
    return TESip, TESport, QID


def _submit(tesip, tesport, SID, QID, answers):
    # 1' send "RQS SID QID V1 V2 V3 V4 V5\n" to TES server
    tcp = TCP(tesip, tesport)

    message = ['RQS', SID, QID]
    message.extend([ans.upper() if ans in ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd'] else 'N' for ans in answers])
    message = '{}\n'.format(' '.join(message))
    data = tcp.request(message)

    # 2' handling response from request to TES server
    # 2.1' error (ERR) - something unexpected happen
    if data.startswith('ERR'):
        log.debug("ERR occur from TCP request to TES.")
        log.error("ERR - There was na error connection to TES server. Try again later.")
        return
    # 2.2' error (-1) - answers submited after the deadline
    if data.startswith('-1'):
        log.debug("-1 occur from TCP request to TES.")
        log.error("-1 - Questionnaire submited after the deadline.")
        return
    # 2.3' error (-1) - answers submited after the deadline
    if data.startswith('-2'):
        log.debug("-2 occur from TCP request to TES.")
        log.error("-2 - This quiz \"{}\" was not created for this student {}.".format(QID, SID))
        return
    # 2.4' returns message
    else:
        log.debug("No errors connecting to TES with TCP Protocol.")
        data = data.split(" ")
        print("Obtained Score {}%".format(data[2]))

if __name__ == "__main__":
    log.debug("Starting client...")

    # format of command is ./user SID [-n ECPname] [-p ECPport]
    # only (size) 6 arguments is allowed
    args = handle_args(sys.argv, allowed_arguments=5 + 1, error_msg='./user SID [-n ECPname] [-p ECPport]')

    ECPname = args.get('-n', settings.DEFAULT_ECPname)
    ECPport = args.get('-p', settings.DEFAULT_ECPport)

    # hack for now.
    SID = sys.argv[1]

    TESip, TESport, QID = None, None, None

    log.debug("Using SID = {}, ECPname = {}, ECPport = {}.".format(SID, ECPname, ECPport))

    # forever
    while(True):
        # waits for client input:
        input_data = raw_input()
        # handle which command should run
        if input_data == 'list':
            # list - chama o ECP com UDP as protocol. pede a lista de topicos
            log.debug("Requesting list of topics to ECP server.")
            _list(ECPname, ECPport)

        elif input_data.startswith('request'):
            # request - Topic NUm (Tnn) por TCP chama o TES respectivo
            log.debug("Requesting information from ECP server about the TES server for that topic.")
            topic_num = input_data.replace('request', '').strip()
            TESip, TESport, QID = _request(ECPname, ECPport, topic_num, SID)

        elif input_data.startswith('submit'):
            # submit <answers_sequece> - TCP Tes resposta
            log.debug("Submiting answers to TES server.")
            answers = filter(None, input_data.replace('submit', '').strip().split(" "))

            if TESip and TESport and QID:
                _submit(TESip, TESport, SID, QID, answers)
            else:
                log.debug("No TESip or TESport.")
                log.error("No TESip or TESport. Request first a topic and then submit your answers.")

        elif input_data == 'exit':
            # exit - exit
            log.debug("Exiting user application.")
            break
        else:
            if input_data.strip() != '':
                log.warning("\"{}\" command does not exist.".format(input_data))
