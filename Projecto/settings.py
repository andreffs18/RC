# !/usr/bin/python
# -*- coding: utf-8 -*-
import os

DEBUG_USER = True
DEBUG_TES = True
DEBUG_ECP = True

# buffer size is equal to 1024bytes*4*1024 = 4mb
BUFFERSIZE = 4096 * 1024

# ECP Configuration
DEFAULT_ECPname = 'localhost'
DEFAULT_ECPport = 58054

# TES Configuration
DEFAULT_TESname = 'localhost'
DEFAULT_TESport = 59000

FAKE_DATABASE = "db.txt"
TOPICS_FILE = "topics.txt"
STATS_FILE = "stats.txt"

QUIZ_PATH = os.getcwd() + "/quiz"
USER_QUIZ_PATH = os.getcwd() + "/user_quizes"
# this value will be added to the current date
DEADLINE_DELTA = 50

# timout after this amout of seconds
TIMEOUT_DELAY = 5

