from cheat_server.exceptions import UnexpectedActionError


class State(object):

    def on_join(self):
        raise UnexpectedActionError("unexpected action `join`")

    def on_deal(self):
        raise UnexpectedActionError("unexpected action `deal`")

    def on_play(self, *, player, cards, quote):
        raise UnexpectedActionError("unexpected action `play`")

    def on_fold(self, *, player, cards, quote):
        raise UnexpectedActionError("unexpected action `fold`")

    def on_call(self, *, player, cards, quote):
        raise UnexpectedActionError("unexpected action `call`")


class WaitingForPlayersState(State):
    """
    The game is afoot, but not everyone is here yet.
    """

    @property
    def num_players(self):
        return self.__num_players

    def __init__(self, *, num_players):
        self.__num_players = num_players

    def on_join(self):
        ...


class WaitingStartMoveState(State):
    """
    Waiting for the first move to be made.  Cards should be dealt evenly, and
    there should be nothing in the `played` or `discard` piles.

    The player with the three of hearts goes first.  They must play it face up,
    optionally with any other threes that they have in their hand.
    """

    def __init__(
        self, *, table,
    ):
        self.__table = table

    def on_play(self, *, player, cards, quote):
        # The cards must be held by the player.
        # One of the cards must be the three of hearts.
        # All cards must have rank three.
        # The number of cards must match the number claimed.
        # The claim must have rank three.
        ...


class WaitingRestartMoveState(State):
    """
    The previous round ended with a player picking up the cards from the in-
    play pile or the in-play being discarded.

    The next player can restart the round.
    """

    def __init__(
        self, *, next_player, table,
    ):
        self.__next_player = next_player
        self.__table = table

    def on_play(self, *, player, cards, quote):
        # The cards must be held by the player.
        # The claimed number of cards must be greater than or equal to one.
        # The claimed number of cards must be less than or equal to six.
        # There is no restriction on rank.
        # The number of cards must match the number claimed.
        ...


class WaitingForNextMoveState(State):
    """
    A round is in progress and at least one move is in progress.

    The next player may play (or pretend to play) a matching number of cards
    of the same or greater rank, fold and move all of the played cards to the
    discard pile, or call out the previous player for their lies.
    """

    def __init__(
        self, *, next_player, table, last_move,
    ):
        self.__next_player = next_player
        self.__table = table
        self.__last_move

    def on_play(self, *, player, cards, claim):
        # The cards must be played by the player to the left of the previous
        # player.
        # The cards must be held by that player.
        # The number claimed must match the previous claim.
        # The rank claimed must be greater than or equal to the previous claim.
        # The number of cards must match the number claimed.
        ...

    def on_fold(self, *, player):
        # The fold must be requested by the player to the left of the previous
        # player.
        ...

    def on_call(self, *, player):
        # There is no restriction on what player can call cheat.  A player can
        # call cheat on themselves if they really want to.
        ...
