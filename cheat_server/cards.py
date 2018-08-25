_undefined = object()


ALL_RANKS = frozenset([
    'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    'Jack', 'Queen', 'King',
])


ALL_SUITS = frozenset([
    'Spades', 'Clubs', 'Diamonds', 'Hearts',
])


ALL_CARDS = frozenset([
    '{rank}_of_{suit}'.format(rank=rank, suit=suit)
    for rank in ALL_RANKS for suit in ALL_SUITS
] + ['Red_Joker', 'Black_Joker'])


def rank(card):
    if card not in ALL_CARDS:
        raise ValueError("invalid card: {card!r}".format(card=card))

    if card in {'Red_Joker', 'Black_Joker'}:
        return 'Joker'

    rank, suit = card.split('_of_')
    return rank


def suit(card):
    if card not in ALL_CARDS:
        raise ValueError("invalid card: {card!r}".format(card=card))

    if card in {'Red_Joker', 'Black_Joker'}:
        return 'Joker'

    rank, suit = card.split('_of_')
    return suit


def _validate_rank(value):
    if not isinstance(value, str):
        raise TypeError(
            f"expected 'string' but value is of type {type(value)!r}"
        )

    if value not in ALL_RANKS:
        raise ValueError(f"string {value!r} does not identify a valid rank")


def validate_rank(value=_undefined):
    def validate(value):
        _validate_rank(value)

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_suit(value):
    if not isinstance(value, str):
        raise TypeError(
            f"expected 'string' but value is of type {type(value)!r}"
        )

    if value not in ALL_SUITS:
        raise ValueError(f"string {value!r} does not identify a valid suit")


def validate_suit(value=_undefined):
    def validate(value):
        _validate_suit(value)

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_card(value):
    if not isinstance(value, str):
        raise TypeError(
            f"expected 'string' but value is of type {type(value)!r}"
        )

    if value not in ALL_CARDS:
        raise ValueError(f"string {value!r} does not identify a real card")


def validate_card(value=_undefined):
    def validate(value):
        _validate_card(value)

    if value is not _undefined:
        validate(value)
    else:
        return validate
