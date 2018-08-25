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


class WaitingForNextMoveState(State):
    """
    A round is in progress and at least one move is in progress.

    The next player may play (or pretend to play) a matching number of cards
    of the same or greater rank, fold and move all of the played cards to the
    discard pile, or call out the previous player for their lies.
    """

    def __init__(
        self, *, next_player, table, last_claim,
    ):
        self.__next_player = next_player
        self.__table = table
        self.__last_claim

    def on_play(self, *, player, cards, claim):
        # === Preconditions ===
        # The cards must be played by the player to the left of the previous
        # player.

        # All of played cards must be held by that player.

        # The number claimed must match the previous claim.

        # The rank claimed must be greater than or equal to the previous claim.

        # The number of cards must match the number claimed.

        # === Outcomes ===
        # If a player other than the current player has no cards left then that
        # player wins.

        # The claim is registered and the cards moved to the played pile.
        # Control goes to the next player.
        ...

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

    def __init__(self, *, winner):
        pass

    def on_deal(self, *, player):
        # === Preconditions ===
        # The player who holds the three of hearts always goes first so there
        # is not need to restrict who can deal.

        # === Outcomes ===
        # Cards are dealt evenly to all of the players on the table
        ...
