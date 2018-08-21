RANKS = frozenset([
    'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    'Jack', 'Queen', 'King',
])


SUITS = frozenset([
    'Spades', 'Clubs', 'Diamonds', 'Hearts',
])


ALL_CARDS = frozenset([
    '{rank}_of_{suit}'.format(rank=rank, suit=suit)
    for rank in RANKS for suit in SUITS
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
