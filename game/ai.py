#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
ai.py

Attempts to make a smart move to
get the deck value as close as it
can to 99
"""

from player import Player
from util import printIfDebug


class AI(Player):
    """Constructor: Creates an AI
    @param name: Name of the AI, usually AI<Some number>
    @param tokens: Number of tokens it starts off with"""
    def __init__(self, name, tokens):
        Player.__init__(self, name, tokens)

        # Game logic
        self.useless_cards = [5, 6, 7, 8]  # No strategic value
        self.possibly_useful = [1, 2, 3, 11, 12]  # Some strategic value later on
        self.small_cards = [1, 2, 3]  # To play when total > 90
        self.last_ditch_effort = [9, 13, 10]  # Worth 0 or subtract, to skip turn
        self.most_valuable = [4]  # Preserve till the end
        self.plus_10 = [11, 12]  # Adds 10 to the total
        self.important = self.last_ditch_effort + self.most_valuable

    def getMove(self, current_total, max_total):
        """getMove: Returns an index from its own cards to play and the value
        to play in an array format [index, value]

        @param current_total: The current game total
        @param max_total: Total cannot go over this number"""

        current_hand = [str(x) for x in self.cards]

        # Eliminate least useful cards first
        card_to_play = self.getValidCards(lambda x: x in self.useless_cards,
                                          current_total, max_total)
        if len(card_to_play) > 0:  # Return largest card
            card_to_play = max(card_to_play)
            printIfDebug("Eliminating useless card: {}. Current hand: {}".format(card_to_play, current_hand))
            return [self.getIndexFromValue(card_to_play.value), card_to_play.value]

        # Ultimate strategy: Play a 9 if you have at
        # least 2 other high value cards
        if len(list(filter(lambda x: x.value in self.important, self.cards))) == 3 and 9 in [x.value for x in
                                                                                             self.cards]:
            printIfDebug("Attempting to go for 99 strategy: Current hand {}".format(current_hand))
            return [self.getIndexFromValue(9), 9]

        # Consider using an Ace, 2 or 3 if score > 90
        if current_total > 90:
            card_to_play = self.getValidCards(lambda x: x in self.small_cards, current_total, max_total)
            if len(card_to_play) > 0:  # Return largest card
                card_to_play = max(card_to_play)
                printIfDebug("Playing small card: {}. Current hand: {}".format(card_to_play, current_hand))
                return [self.getIndexFromValue(card_to_play.value), card_to_play.value]

        # Consider using jack or queen
        card_to_play = self.getValidCards(lambda x: x in self.plus_10, current_total, max_total)
        if len(card_to_play) > 0:
            card_to_play = max(card_to_play)
            printIfDebug("Playing +10: {}. Current hand: {}".format(card_to_play, current_hand))
            return [self.getIndexFromValue(card_to_play.value), card_to_play.value]

        # Consider king
        card_to_play = self.getValidCards(lambda x: x == 13, current_total, max_total)
        if len(card_to_play) > 0:
            printIfDebug("Skipping turn: {}. Current hand: {}".format(max(card_to_play), current_hand))
            return [self.getIndexFromValue(13), 13]

        # Consider using 10 (+ or - 10)
        if self.getIndexFromValue(10) != -1:
            print("Playing 10. Current hand: {}".format(current_hand))
            if current_total + 10 <= max_total:
                return [self.getIndexFromValue(10), 10]
            else:
                return [self.getIndexFromValue(10), -10]

        # Consider valuable cards
        card_to_play = self.getValidCards(lambda x: x in self.most_valuable, current_total, max_total)
        if len(card_to_play) > 0:
            card_to_play = max(card_to_play)
            printIfDebug("Playing valuable card: {}. Current hand: {}".format(card_to_play, current_hand))
            return [self.getIndexFromValue(card_to_play.value), card_to_play.value]

        # Check all cards to see if you can play one
        card_to_play = self.getValidCards(lambda x: True, current_total, max_total)
        if len(card_to_play) > 0:
            card_to_play = max(card_to_play)
            printIfDebug("Playing any card: {}. Current hand: {}".format(card_to_play, current_hand))
            return [self.getIndexFromValue(card_to_play.value), card_to_play.value]

        # Appears no valid moves can be made
        return [-1, 0]

    def getValidCards(self, allowed, current_total, max_total):
        """returnValidCards: Return all cards in hand where
        allowed(card) is equal to True

        @param allowed: Boolean Function, accepts card value (int as parameter.
        @param current_total: The current game total
        @param max_total: Total cannot go over this number"""
        to_return = []
        for card in self.cards:
            if allowed(card.value) and card.getTrueValue() + current_total <= max_total:
                to_return.append(card)
        return to_return

    def getIndexFromValue(self, value):
        """indexFromValue: Given a value of a card, return index in hand
        @param value: value of card to find"""
        for i in range(len(self.cards)):
            if self.cards[i].value == value:
                return i
        return -1

    def getType(self):
        """Returns type of player"""
        return "ai"
