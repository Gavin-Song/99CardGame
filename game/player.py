#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
player.py

Base class for a player. AI and
Human extend this class
"""

from abc import abstractmethod, ABCMeta
from deck import Deck


class Player(object):
    __metaclass__ = ABCMeta

    def __init__(self, name, tokens):
        self.name = name
        self.cards = Deck()
        self.tokens = tokens

    @abstractmethod
    def getType(self):
        pass

    @abstractmethod
    def getMove(self, current_total, max_total):
        pass

    def isCardPlayable(self, card, total, max_val):
        """isCardPlayable: Is a card value playable?
        @param card: Card object
        @param total: Current game total
        @param max_val: Max game value (99)"""
        return card.getTrueValue() + total <= max_val

    def isMoveValid(self, card, selected_value, total, max_val):
        """isMoveValid: Can you play a card?
        @param card: Card object
        @param selected_value: If a card has a selectable value, the value selected
        @param total: Current game total
        @param max_val: Max game value (99)"""

        if card.value not in [1, 10]:
            return self.isCardPlayable(card, total, max_val)
        if card.value == 10 and selected_value == -10:
            return True
        if card.value == 1:
            return selected_value + total <= max_val
        return True

    def __str__(self):
        """Debug data"""
        return "Name: {} | Tokens: {} | Cards: {}".format(self.name, self.tokens, [str(x) for x in self.cards])
