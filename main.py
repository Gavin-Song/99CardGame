"""
99 Card game

A simple addition based card game. See
https://en.wikipedia.org/wiki/Ninety-nine_(addition_card_game)
for more information.

File name: main.py
Author: Gavin Song
Python Version: 3.6
"""

from game import game
from game import config
from game import command
import time

Game = game.Game
global CURRENT_GAME

def startGame(n=config.DEFAULT_NUM_PLAYERS):
    """Plays a game with n players"""

    n = int(n)
    if n < 2 or n > config.DECK_SIZE / 3: # Invalid player number
        print("     Invalid number of players. The number of players should")
        print("     be between 2 and {}".format(int(config.DECK_SIZE/3)))
        return False

    game = Game()
    game.startGame(n)
    print("")

    while True:
        global CURRENT_GAME
        CURRENT_GAME = game

        # Prompt the current player for a move
        move = game.getCurrentPlayer().getMove(game.TOTAL, game.MAX)
        move_allowed = game.playTurn(move[0], move[1])

        if not move_allowed:  # Player can't make a move at all
            game.getCurrentPlayer().tokens -= 1
            if game.getCurrentPlayer().tokens == 0:
                game.killCurrentPlayer()

            print("\nNO POSSIBLE MOVES, REDISTRIBUTING ALL CARDS\n")
            game.redistributeCards()
            game.TURN += 1  # Game doesn't increment turn if move fails

        print("")

        if len(game.PLAYERS) == 1:
            print("WINNER! {}".format(game.getCurrentPlayer()))
            break

        time.sleep(config.AI_TURN_DELAY)

def gameStats():
    global CURRENT_GAME
    print(CURRENT_GAME)
    CURRENT_GAME.displayStats()

command.addCommand(
    command.Command("stats", "stats - Display current game stats.", gameStats))
command.addCommand(
    command.Command("start", "start [players=4] - Start a game with n players.", startGame))


# Run the actual game
if __name__ == "__main__":
    print(config.TITLE)

    while True:
        user_input = input("> ")
        command.executeCommand(user_input)









