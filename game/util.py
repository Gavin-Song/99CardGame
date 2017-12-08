#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
util.py

Helpful utility functions
"""

from config import DEBUG, CHAR_DELAY
import time

def printIfDebug(args):
    "print: Debug only. Does not print if DEBUG is disabled"
    if DEBUG: print(args)


def slowPrint(args):
    """slowPrint: Slowly print a string
    Delay between characters is CHAR_DELAY"""
    for char in args:
        print(char, end="")
        time.sleep(CHAR_DELAY)
    print("")