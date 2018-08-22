from cheat_server.cards import ALL_CARDS


class Stack(object):
    __slots__ = ['_Stack__cards']

    def __init__(self, cards=[]):
        cards = list(cards)

        for card in cards:
            if card not in ALL_CARDS:
                raise ValueError("invalid card: {card!r}".format(card=card))

        if len(cards) != len(set(cards)):
            raise ValueError("stack contains duplicates")

        self.__cards = cards

    def __contains__(self, card):
        return card in self.__cards

    def __iter__(self):
        return iter(self.__cards)

    def __hash__(self):
        return hash(tuple(self.__cards))

    def __eq__(self, other):
        if type(other) != type(self):
            return NotImplemented

        return self.__cards == other.__cards

    def add(self, cards):
        """
        Creates a new stack with the new cards appended to the end of the
        stack.

        :param cards:
            An iterable of cards to add.

        :raises ValueError:
            If the cards are already in the stack.
        :raises ValueError:
            If the list of cards contains duplicates.
        """
        updated = list(self.__cards)
        for card in cards:
            if card in updated:
                raise ValueError("duplicate card: {card!r}".format(card=card))
            updated.append(card)

        return Stack(updated)

    def remove(self, cards):
        """
        Creates a new stack with the requested cards removed.

        Preserves the order of the remaining cards.

        :param cards:
            An iterable of cards to remove.

        :raises ValueError:
            If any of the cards are missing from the stack.
        """
        updated = list(self.__cards)
        for card in cards:
            # Raises ValueError if card is missing.
            updated.remove(card)

        return Stack(updated)

