#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
config.py

Config file. What did you expect?
Edit any game variables here
"""

# Should it display debug messages?
DEBUG = False

# Some card naming variables
SUITS = ["clubs", "diamonds", "hearts", "spades"]
CARD_MAP = {  # Maps named card numbers to a name
    11: "Jack",
    12: "Queen",
    13: "King"
}
SUIT_MAP = {  # Maps suit to unicode character
    "clubs": u"\u2663",
    "diamonds": u"\u2666",
    "hearts": u"\u2764",
    "spades": u"\u2660"
}


DECK_SIZE = 52  # Size of the deck
SUIT_SIZE = len(SUITS)  # Cards per suit
DEFAULT_NUM_PLAYERS = 4  # Default number of players

# Cards that don't follow the "add the value" rule
SPECIAL_CARDS = [3, 4, 10, 9, 11, 12, 13, 1]

CHAR_DELAY = 0.04  # Delay between printing characters
AI_TURN_DELAY = 2  # Delay between AI moves

TITLE = """
    _   ___            __                    _          
   / | / (_)___  ___  / /___  __      ____  (_)___  ___ 
  /  |/ / / __ \\/ _ \\/ __/ / / /_____/ __ \\/ / __ \\/ _ \\
 / /|  / / / / /  __/ /_/ /_/ /_____/ / / / / / / /  __/
/_/ |_/_/_/ /_/\\___/\\__/\\__, /     /_/ /_/_/_/ /_/\\___/ 
                       /____/                           

:::::::::::::::::::: - HELP - ::::::::::::::::::::
Type a command to execute it

start [player_num=4] : Start a new game, optionally with n players
help [command]       : View help, optionally for a specific command 
rules                : View game rules 
quit                 : Quit the current game 

Tip: Type "start" to start a new game 
"""

