# !/usr/bin/python
# -*- coding: utf-8 -*-
import os

DEBUG_USER = True
DEBUG_TES = True
DEBUG_ECP = True

# buffer size is equal to 1024mb*4 = 4mb
BUFFERSIZE = 4096

# ECP Configuration
DEFAULT_ECPname = 'localhost'
DEFAULT_ECPport = 58054

# TES Configuration
DEFAULT_TESname = 'localhost'
DEFAULT_TESport = 59000

FAKE_DATABASE = "db.txt"
TOPICS_FILE = "topics.txt"
STATS_FILE = "stats.txt"

QUIZ_PATH = os.getcwd() + "/quizes"
USER_QUIZ_PATH = os.getcwd() + "/user_quizes"

DEADLINE_HOUR = 12
DEADLINE_MINUTE = 50
DEADLINE_SECOND = 00
