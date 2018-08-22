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

    def __repr__(self):
        return f"Stack([{', '.join(self)}])"


class Table(object):
    """
    Immutable class that describes the location of all of the cards in a deck.
    """

    __slots__ = ['_Table__hands', '_Table__played', '_Table__discarded']

    @property
    def hands(self):
        """
        Returns a tuple of cards stack with each stack corresponding to the
        hand of the player with the same index.

        This is semantically a list, but lists can't be frozen.  An iterator
        makes no sense as user will almost always want to index the result.
        """
        return self.__hands

    @property
    def played(self):
        """
        Returns the stack of cards that have been played in this round.
        """
        return self.__played

    @property
    def discarded(self):
        """
        Returns the stack of cards that have been removed from play.
        """
        return self.__discarded

    def __init__(self, *, hands, played, discarded):
        hands = tuple(hands)
        for hand in hands:
            if not isinstance(hand, Stack):
                raise TypeError((
                    "expected 'Stack' but hand is of type {cls}"
                ).format(cls=type(played).__name__))
        self.__hands = hands

        if not isinstance(played, Stack):
            raise TypeError((
                "expected 'Stack' but played is of type {cls}"
            ).format(cls=type(played).__name__))
        self.__played = Stack(played)

        if not isinstance(discarded, Stack):
            raise TypeError((
                "expected 'Stack' but discarded is of type {cls}"
            ).format(cls=type(discarded).__name__))
        self.__discarded = Stack(discarded)

    @classmethod
    def deal(cls, cards):
        """
        Creates a fresh table and deals the deck of cards out evenly between
        the two players.  Player 0 is assumed to be the dealer.
        """
        # Deal each player every second card.  The dealer always starts by
        # dealing to the next player.
        hands = [
            Stack(cards[1::2]),
            Stack(cards[::2]),
        ]

        # New game so played and discarded are empty.
        played = Stack()
        discarded = Stack()

        return Table(
            hands=hands,
            played=played,
            discarded=discarded,
        )

    def play(self, *, player, cards):
        """
        Moves selected cards from player hand to the played pile.

        Raises an exception if the card does not have the requested cards.
        """
        # The requested cards are removed from the players hand.  This will
        # raise :exception:`IndexError` if the player does not exist and
        # :exception:`ValueError` if they do not possess the requested cards.
        hands = list(self.hands)
        hands[player] = hands[player].remove(cards)

        # The cards from the players hand are added to the played pile.
        played = self.played.add(cards)

        # The discard pile is unaffected.
        discarded = self.discarded

        return Table(
            hands=hands,
            played=played,
            discarded=discarded,
        )

    def fold(self):
        """
        Returns a copy of the table with all cards from the `played` stack
        moved to the `discarded` stack.
        """
        # Player's hands are unaffected.
        hands = list(self.hands)

        # The played stack is emptied.
        played = Stack()

        # Played cards are added to the discard pile.
        discarded = self.discarded.add(self.played)

        return Table(
            hands=hands,
            played=played,
            discarded=discarded,
        )

    def collect(self, *, player):
        """
        Creates a copy of the table with all cards from the `played` stack
        movedto a player's hand.
        """
        # Cards from the played pile are moved to the selected players hand.
        hands = list(self.hands)
        hands[player] = hands[player].add(self.played)

        # The played stack is emptied.
        played = Stack()

        # The discarded stack is unaffected.
        discarded = self.discarded

        return Table(
            hands=hands,
            played=played,
            discarded=discarded,
        )
