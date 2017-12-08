#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
command.py

Commands to type into the terminal
"""

from util import printIfDebug

commands = []

class Command(object):
    def __init__(self, name, help_text, run):
        self.name = name
        self.help_text = help_text
        self.run = run

def addCommand(command):
    """Adds a Command object to the command array
    @param command: A Command object"""
    commands.append(command)

def executeCommand(user_input):
    """Executes the command given user_input string,
    returns True if execution is successful"""

    if user_input.lstrip().rstrip() == "":
        return False

    args = user_input.split(" ")
    cmd_name = args[0]

    for command in commands:
        if command.name == cmd_name:
            try:
                if len(args) == 1:
                    command.run()
                elif len(args) > 1: # Sorry only supports 1 arg commands
                    command.run(args[1])
                return True
            except Exception as e:
                printIfDebug(e)
                return False

    return False


# ------------ Commands ------------- #
def rules():
    """Outputs the game rules"""

    print("""
    ----- Rules ----
    
    Each player starts out with 3 tokens. Each hand (3 cards)
    are dealt to each player. Each player places one of their 
    cards onto a pile, then draws another card. Keep playing 
    until a player cannot place a card without going over 99,
    in which case all cards are collected, shuffled, and 
    redistributed. 
    
    The total starts at 0, and every time a card is placed
    the total is incremented by the card's face value (With
    the following exceptions:)
    
    Ace: Worth 1 or 11 (Choose a value)
    3:   Worth 3, but next player skips a turn
    4:   Worth 0, reverses turn order
    9:   Sets value to 99, regardless of previous value
    10:  Worth +10 or -10 (Choose a value)
    J:   Worth +10
    Q:   Worth +10
    K:   Worth 0
    """)

def quit():
    """Prompts player to quit the game"""
    prompt = input("Are you sure you want to quit? (Y/N): ")
    if prompt.lower() == "y":
        __import__("sys").exit()
    return False

def help_cmd(command="help"):
    for cmd in commands:
        if cmd.name == command:
            print("     " + cmd.help_text)
            return
    print("     Could not find the command")

addCommand(Command("rules", "rules - Display the game rules", rules))
addCommand(Command("quit", "quit - Quit the game", quit))
addCommand(Command("help", "help [command] - Get help for a command", help_cmd))