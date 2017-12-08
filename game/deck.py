#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
deck.py

The Card and Deck class, handles keeping track of
the cards and deck function.
"""

import config
import random


class Card(object):
    """Constructor: Creates a card object
    @param value: A number 1-13 representing the card value
    @param suit: A lowercase string representing the card suit"""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def getName(self):
        """getName: Returns the name of the card
        Example: King of spades"""
        if self.value < 11:
            return "{} of {}".format(self.value, self.suit)
        elif self.value < 14:
            return "{} of {}".format(config.CARD_MAP[self.value], self.suit)
        return "Unknown card."

    def prettyName(self):
        """prettyName: Pretty prints the name
        with unicode suit symbols"""
        if self.value < 11:
            return "{}{}".format(self.value, config.SUIT_MAP[self.suit])
        elif self.value < 14:
            return "{}{}".format("JQK"[self.value - 11], config.SUIT_MAP[self.suit])
        return "--"

    def isSpecial(self):
        """isSpecial: Does the card do anything special?"""
        return self.value in config.SPECIAL_CARDS

    def getTrueValue(self):
        """Returns the true "value" it represents
        Some cards that can add <= 0 value return 0"""
        if self.value in [4, 10, 9, 13]:
            return 0
        return self.value

    def getDescription(self):
        """Returns a description of the card"""

        if self.value == 4:
            return "(+0) Reverses turn order (Unless there are only 2 players)"
        if self.value == 3:
            return "(+3) Skips next player's turn (Unless there are only 2 players)"
        if self.value == 10:
            return "(+10 or -10) Choose value"
        if self.value == 1:
            return "(+1 or +11) Choose value"
        if self.value == 9:
            return "Sets the total to 99 regardless of previous value"
        if self.value in [11, 12]:
            return "(+10)"
        if self.value == 13:
            return "(+0) Skip your turn"
        return "(+{})".format(self.value)

    # str(card) should return the pretty name
    # rather than the long string name
    def __str__(self):
        return self.prettyName()

    # cards are equal if they have the same value
    # and suit. (Although game only compares value)
    def __eq__(self, other):
        return other.value == self.value and other.suit == self.suit

    def __ne__(self, other):
        return not self.__eq__(other)

    # Uses the card value, not the true value
    # for size comparision
    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value


class Deck(object):
    """Constructor: Creates an empty deck"""
    def __init__(self):
        self.cards = []

    def shuffle(self):
        """Shuffles the cards in place"""
        random.shuffle(self.cards)

    def removeTopCard(self):
        """Removes and returns top card
        IndexError if there are no cards"""
        return self.cards.pop(0)

    def addCard(self, card):
        """Adds a new card to the bottom of the deck
        @param card: A Card object"""
        self.cards.append(card)

    def removeAllCards(self):
        """Clears the deck of all cards"""
        self.cards = []

    # Returns how many cards are the deck
    def __len__(self):
        return len(self.cards)

    # For getting a card by index, for example
    # deck[0] should return the first card
    def __getitem__(self, key):
        return self.cards[key]