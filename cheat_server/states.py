from validation import validate_list, validate_int

from cheat_server.cards import validate_card, validate_rank
from cheat_server.table import validate_table
from cheat_server.exceptions import UnexpectedActionError

_undefined = object()

_RANK_ORDER = [
    '3', '4', '5', '6', '7', '8', '9', '10',
    'Jack', 'Queen', 'King',
    'Ace', '2',
]


class Claim(object):

    __slots__ = ['_Claim__rank', '_Claim__count']

    @property
    def rank(self):
        return self.__rank

    @property
    def count(self):
        return self.__count

    def __init__(self, rank, count):
        validate_rank(rank)
        self.__rank = rank

        validate_int(count, min_value=1, max_value=6)
        self.__count = count


def _validate_claim(value):
    if not isinstance(value, Claim):
        raise TypeError(
            f"expected 'Claim' but value is of type {type(value)!r}"
        )


def validate_claim(value=_undefined):
    def validate(value):
        _validate_claim(value)

    if value is not _undefined:
        validate(value)
    else:
        return validate


class State(object):

    def on_deal(self, *, player):
        raise UnexpectedActionError("unexpected action `deal`")

    def on_play(self, *, player, cards, quote):
        raise UnexpectedActionError("unexpected action `play`")

    def on_fold(self, *, player, cards, quote):
        raise UnexpectedActionError("unexpected action `fold`")

    def on_call(self, *, player, cards, quote):
        raise UnexpectedActionError("unexpected action `call`")


class StartedState(State):
    """
    Waiting for the first move to be made.  Cards should be dealt evenly, and
    there should be nothing in the `played` or `discard` piles.

    The player with the three of hearts goes first.  They must play it face up,
    optionally with any other threes that they have in their hand.
    """

    @property
    def table(self):
        return self.__table

    def __init__(
        self, *, table,
    ):
        validate_table(table)
        self.__table = table

    def on_play(self, *, player, cards, quote):
        # === Preconditions ===
        # The number of cards must match the number claimed.

        # The claim must have rank three.

        # All cards must have rank three.

        # One of the cards must be the three of hearts.

        # The cards must be held by the player.

        # === Outcomes ===
        # The claim is recorded and cards moved to the played pile.  Control
        # goes to the next player.
        ...


class RestartedState(State):
    """
    The previous round ended with a player picking up the cards from the in-
    play pile or the in-play being discarded.

    The next player can restart the round.
    """

    @property
    def next_player(self):
        return self.__next_player

    @property
    def table(self):
        return self.__table

    def __init__(
        self, *, next_player, table,
    ):
        validate_table(table)
        self.__table = table

        validate_int(next_player, min_value=0, max_value=len(table.hands))
        self.__next_player = next_player

    def on_play(self, *, player, cards, quote):
        # === Preconditions ===
        # The cards must be held by the player.

        # The claimed number of cards must be greater than or equal to one.

        # The claimed number of cards must be less than or equal to six.

        # There is no restriction on rank.

        # The number of cards must match the number claimed.

        # === Outcomes ===
        # The claim is recorded and cards moved to the played pile.  Control
        # goes to the next player.
        ...


class InPlayState(State):
    """
    A round is in progress and at least one move is in progress.

    The next player may play (or pretend to play) a matching number of cards
    of the same or greater rank, fold and move all of the played cards to the
    discard pile, or call out the previous player for their lies.
    """

    @property
    def next_player(self):
        return self.__next_player

    @property
    def table(self):
        return self.__next_player

    @property
    def last_claim(self):
        return self.__last_claim

    def __init__(
        self, *, next_player, table, last_claim,
    ):
        validate_table(table)
        self.__table = table

        validate_int(next_player, min_value=0, max_value=len(table.hands))
        self.__next_player = next_player

        validate_claim(last_claim)
        self.__last_claim

    def on_play(self, *, player, cards, claim):
        validate_int(player)
        validate_list(validator=validate_card(), min_length=1, max_length=6)
        validate_claim(claim)

        # === Preconditions ===
        # The cards must be played by the player to the left of the previous
        # player.
        if player != self.next_player:
            raise Exception()

        # All of played cards must be held by that player.
        for card in cards:
            if card not in self.table.hands[player]:
                raise Exception("can not play card that is not held")

        # The number claimed must match the previous claim.
        if claim.count != self.last_claim.count:
            raise Exception("claim count must match previous claim")

        # The rank claimed must be greater than or equal to the previous claim.
        if (
            _RANK_ORDER.index(claim.rank) <
            _RANK_ORDER.index(self.last_claim.rank)
        ):
            raise Exception("claim rank must meet or exceed previous claim")

        # The number of cards must match the number claimed.
        if len(cards) != claim.count:
            raise Exception("number of cards played does not match claim")

        # === Outcomes ===
        # If a player other than the current player has no cards left then that
        # player wins.  We run this check before moving the cards as doing so
        # means that the player will definitely still be holding some cards.
        for possible_winner, hand in enumerate(self.table.hands):
            if not hand:
                return VictoryState(winner=possible_winner)

        # The claim is registered and the cards moved to the played pile.
        # Control goes to the next player.
        next_player = (player + 1) % len(self.table.hands)
        table = self.table.play(cards)
        return InPlayState(
            next_player=next_player, table=table, last_claim=claim,
        )

    def on_fold(self, *, player):
        # === Preconditions ===
        # The fold must be requested by the player to the left of the previous
        # player.

        # === Outcomes ===
        # If a player other than the current player has no cards left then that
        # player wins.

        # Cards in the played pile are moved to the discard pile. Control goes
        # to the next player to restart the bidding.
        ...

    def on_call(self, *, player):
        # === Preconditions ===
        # There is no restriction on what player can call cheat.  A player can
        # call cheat on themselves if they really want to.

        # === Outcomes ===
        # If the cards at the top of the played pile match the claim then the
        # player who called cheat collects the cards and play resumes from
        # the player to their left.

        # If the cards at the top of the played pile do not match the claim
        # then the player who played them must collect and the player who
        # called cheat gets the next move.
        ...


class VictoryState(State):
    """
    One of the players has no cards left, and has survived the next player's
    turn without being successfully called out.  They win!
    """
    @property
    def winner(self):
        return self.__winner

    def __init__(self, *, winner):
        validate_int(winner, min_value=0)
        self.__winner = winner

    def on_deal(self, *, player):
        # === Preconditions ===
        # The player who holds the three of hearts always goes first so there
        # is not need to restrict who can deal.

        # === Outcomes ===
        # Cards are dealt evenly to all of the players on the table
        ...
