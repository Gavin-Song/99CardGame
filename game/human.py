#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
human.py

Human player. Accepts input form the
console to make moves.
"""

from player import Player
import command


class Human(Player):
    """Constructor: Creates a Human
    @param name: Name of the Human, usually MAN
    @param tokens: Number of tokens it starts off with"""
    def __init__(self, name, tokens):
        Player.__init__(self, name, tokens)

    def promptSelectedValue(self, allowed_values):
        """promptSelectedValue: Used when a card has more than 1
        value. Prompts the user to select one of the values.

        @param allowed_values: An array of the values that the card
            can act as, such as [1,11]. An input of 1 would mean an index
            of 0, an input of 2 means an index of 1, etc... (In general
            input value is index + 1)

            For example, with the above example if the user inputted 2 it would
            return 1.

        If the selected value is not valid, it will keep prompting the user"""

        index = 1
        for value in allowed_values:
            value_pretty = "+" + str(value) if value >= 0 else str(value)
            print("[{}] :   {}".format(index, value_pretty))
            index += 1

        selected_value = 0
        while selected_value not in allowed_values:
            try:
                index = int(input("Please make a selection: "))
                selected_value = allowed_values[index - 1]
            except:
                print("Not a valid choice, please choose from {}".format(
                    ", ".join([str(x) for x in range(1, len(allowed_values) + 1)])))
        return selected_value

    def getMove(self, current_total, max_total):
        """getMove: Prompts the user for a move.
        @param current_total: The current game total
        @param max_total: Max game total (99)"""

        print("\n")
        print("+------------ Your Cards -----------+")

        unplayable_cards = []
        option = 1
        for card in self.cards:
            print("[{}] :  {} {}".format(option, card, card.getDescription()))
            if not self.isCardPlayable(card, current_total, max_total):
                unplayable_cards.append(card)
            option += 1
        print("+------------------------------------+")

        # If the user has 1 or 2 unplayable cards, then display a tip
        # stating that the user cannot play those cards
        if 3 > len(unplayable_cards) > 0:
            list_unplayable_cards = ", ".join([str(x) for x in unplayable_cards])
            print("\n[TIP] Cards you cannot play: {}".format(list_unplayable_cards))

        # If the user cannot play any cards, they must surrender
        elif len(unplayable_cards) == 3:
            print("\nYou cannot make any moves. Press ENTER to continue")
            input("> ")
            return [-1, 0]

        # Prompt the user to select the actual card
        player_option = 0
        while not 1 <= player_option <= len(self.cards):
            display_error = True

            try:
                player_option = input("\nPlease select a card: ")

                # User can also run commands instead of selecting cards
                player_cmd = command.executeCommand(player_option)
                if player_cmd:
                    player_option = "notanumber"
                    display_error = False

                player_option = int(player_option)
            except ValueError:
                if display_error:
                    print("Your card must be a number listed above.")
                player_option = -1
        player_option -= 1

        # If the card has selectable values then
        # prompt the user to choose those values
        selected_value = 0

        if self.cards[player_option].value == 1:
            print("Ace can be either +1 or +11. Please make a choice:")
            selected_value = self.promptSelectedValue([1, 11])

        elif self.cards[player_option].value == 10:
            print("10 can be either -10 or 10. Please make a choice:")
            selected_value = self.promptSelectedValue([10, -10])

        # If the choice is not valid, then keep
        # prompting the user until they make a valid choice
        if not self.isMoveValid(self.cards[player_option], selected_value, current_total, max_total):
            print("You cannot play that card or value!\n")
            return self.getMove(current_total, max_total)
        print("\n\n")

        return [player_option, selected_value]

    def getType(self):
        """Returns the type of the player"""
        return "human"
