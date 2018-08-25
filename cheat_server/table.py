from cheat_server.cards import ALL_CARDS
from cheat_server.stack import Stack


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
        self.__played = played

        # Check discarded.
        if not isinstance(discarded, Stack):
            raise TypeError((
                "expected 'Stack' but discarded is of type {cls}"
            ).format(cls=type(discarded).__name__))
        self.__discarded = discarded

        # Check that table has been constructed with exactly one deck of cards.
        cards = []
        for hand in hands:
            cards += list(hand)
        cards += list(played)
        cards += list(discarded)

        if set(cards) != ALL_CARDS:
            raise AssertionError("cards missing from table")

        if len(cards) > len(ALL_CARDS):
            raise AssertionError("table contains duplicate cards")

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
