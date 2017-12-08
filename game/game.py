#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
game.py

The actual game logic. A new Game
object is created when a game is started
"""

import sys
import os
sys.path.append(os.getcwd() + "/game")

from ai import AI
from human import Human
from deck import Card, Deck
from config import *
from util import *

import random


class Game(object):
    def __init__(self):
        self.DECK = Deck()  # Deck to draw cards from
        self.PILE = Deck()  # Pile of cards placed on the table
        self.PLAYERS = []  # Array of players

        self.TURN = 0  # Number repersenting the current turn
        self.TURN_INC = 1  # How much to increment TURN each turn

        self.TOTAL = 0  # Number repersenting the total sum
        self.MAX = 99  # TOTAL cannot go over this number.
        self.INITAL_TOKEN = 3  # Inital number of tokens per player
        self.HAND_SIZE = 3  # Cards per player

        # -- Stats -- #
        self.TURNS_TOTAL = 0
        self.PLAYERS_ELIMINATED = 0

    def generateDeck(self):
        """Regenerates the deck, based on the
        config data in config.py"""

        self.DECK.removeAllCards()
        for i in range(int(DECK_SIZE / SUIT_SIZE)):
            for suit in SUITS:
                self.DECK.addCard(Card(i + 1, suit))

    def distributeCards(self):
        """Distributes card from the deck to players.
        If cards run out throws an IndexError Exception"""
        for i in range(len(self.PLAYERS)):
            for k in range(self.HAND_SIZE):
                self.PLAYERS[i].cards.addCard(self.DECK.removeTopCard())

    def redistributeCards(self):
        """Redistributes all cards (Combines PILE, DECK and player cards)
        to the players all over again."""
        for player in self.PLAYERS:
            player.cards.removeAllCards()
        self.PILE = Deck()
        self.generateDeck()
        self.DECK.shuffle()
        self.distributeCards()

    def startGameMessage(self, n):
        """Displays the game loading mesage
        @param n: Number of players in the game"""

        message = """Starting a new game with {} players.
Shuffling the deck... distributing the cards...""".format(n)
        slowPrint(message)

    def startGame(self, n=DEFAULT_NUM_PLAYERS):
        """Start a game with n players
        @param n: The number of players in the game"""
        self.startGameMessage(n)

        # Create the inital deck
        self.generateDeck()
        self.DECK.shuffle()

        # Create the players
        self.PLAYERS = []  # Remove all current players

        # Create n-1 AI players
        for i in range(n - 1):
            self.PLAYERS.append(
                AI(
                    name="AI{}".format(i + 1),
                    tokens=self.INITAL_TOKEN
                )
            )
        # Create the human player
        self.PLAYERS.append(
            Human(
                name="MAN",
                tokens=self.INITAL_TOKEN
            )
        )
        # Shuffle the turn order
        random.shuffle(self.PLAYERS)

        # Distribute cards to players
        self.distributeCards()

    def getCurrentPlayer(self):
        """Returns the current player, based on turn order"""
        return self.PLAYERS[self.TURN % len(self.PLAYERS)]

    def getHumanPlayer(self):
        """Returns the human player"""
        for p in self.PLAYERS:
            if p.getType() == "human":
                return p
        return None

    def playTurn(self, card_index, selected_value=0):
        """The current player plays a card
        @param card_index: The index of the card in player.cards
           they wish to play.

        @param selected_value: Some cards allow the player to select
           a value to play. Ie, if the card is either +10 or -10,
           a possible value for selected_value would be -10

        Returns False if the card is played successfully, otherwise
        returns True"""

        current_player = self.PLAYERS[self.TURN % len(self.PLAYERS)]

        # Index is invalid, should be 0 <= index < cards.length
        if not 0 <= card_index < len(current_player.cards):
            return False

        card_to_play = current_player.cards[card_index]
        to_add = 0

        # Card handling
        # ---------------------------------------------

        # Non-special cards are worth just their value
        if not card_to_play.isSpecial():
            to_add = card_to_play.value

        # 4 is worth 0, reverses order of play
        elif card_to_play.value == 4:
            if len(self.PLAYERS) > 2:
                self.TURN_INC = -self.TURN_INC

                # 3 is worth 3, next player is skipped unless
        # there are only 2 players
        elif card_to_play.value == 3:
            to_add = 3
            if len(self.PLAYERS) > 2:
                self.TURN += self.TURN_INC

                # 10 is either +10 or -10
        elif card_to_play.value == 10:
            if not selected_value in [-10, 10]:
                return False
            to_add = selected_value

        # 9 Changes the value of the deck to 99. (Worth 0)
        elif card_to_play.value == 9:
            self.TOTAL = 99

        # K is worth 0 (Skip)
        elif card_to_play.value == 13:
            pass

            # Queens and jacks are worth 10
        elif card_to_play.value in [11, 12]:
            to_add = 10

            # Aces are worth 1 or 11
        elif card_to_play.value == 1:
            if not selected_value in [1, 11]:
                return False
            to_add = selected_value

        # The total cannot surpass 99.
        if self.TOTAL + to_add > self.MAX:
            return False

        self.TOTAL += to_add
        self.TURN += self.TURN_INC
        self.announceTurn(current_player, card_to_play)

        self.PILE.addCard(current_player.cards.cards[card_index])
        del current_player.cards.cards[card_index]
        current_player.cards.addCard(self.DECK.removeTopCard())

        self.TURNS_TOTAL += 1

        self.checkDeckSize()

        return True

    def announceTurn(self, player, card):
        """Announces a player action and the current game total"""
        print("[{}] {} has played a {}{}.".format(player.name, player.name, card,
                                                  " (Special)" if card.isSpecial() else ""))
        if card.value == 4:
            print("[GAME] Turn order has been reversed!")
        elif card.value == 3:
            print("[GAME] The next player has been skipped.")
        print("[GAME] The current total is {}".format(self.TOTAL))

    def killCurrentPlayer(self):
        """Announces the current player's death and removes them
        from the array"""
        current_player = self.getCurrentPlayer()
        self.PLAYERS_ELIMINATED += 1
        print("[GAME] {} has been eliminated!".format(current_player.name))
        self.PLAYERS.remove(current_player)

    def checkDeckSize(self):
        """If the deck size is 0 collect cards from the PILE
        and reshuffle"""
        if len(self.DECK) == 0:
            print("")
            print("Deck empty, putting cards from the pile back into the deck...")
            slowPrint("Shuffling...")
            print("")

            self.DECK, self.PILE = self.PILE, self.DECK
            self.DECK.shuffle()

    def displayStats(self):
        """Display statistics"""
        player_list = "\n".join(
            list(map(lambda x:
                     "      [{}] Tokens: {}".format(x.name, x.tokens),
                     self.PLAYERS))
        )

        tokens = 0
        human_player = self.getHumanPlayer()
        if human_player is not None:
            tokens = human_player.tokens

        print("""
            -- Current Game Stats --
        {}

            Turns passed:       {}
            Players eliminated: {}
            Your tokens:        {} 
            """.format(player_list, self.TURNS_TOTAL, self.PLAYERS_ELIMINATED,
                       tokens))
