import unittest
import itertools

from cheat_server.cards import ALL_CARDS, ALL_RANKS, ALL_SUITS, rank, suit


class CardsTestCase(unittest.TestCase):

    def test_no_overlap(self):
        self.assertEqual(
            set.intersection(set(ALL_RANKS), set(ALL_SUITS)),
            set(),
        )

    def test_size(self):
        self.assertEqual(len(ALL_CARDS), 54)


class RankTestCase(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(rank('Ace_of_Spades'), 'Ace')

    def test_jokers(self):
        self.assertEqual(rank('Red_Joker'), 'Joker')
        self.assertEqual(rank('Black_Joker'), 'Joker')

    def test_invalid_suit(self):
        with self.assertRaises(ValueError):
            rank('11_of_Hearts')

    def test_flipped(self):
        for rank_, suit_ in itertools.product(ALL_RANKS, ALL_SUITS):
            card = '{suit}_of_{rank}'.format(rank=rank_, suit=suit_)
            with self.assertRaises(ValueError):
                rank(card)

    def test_capitalised(self):
        for rank_, suit_ in itertools.product(ALL_RANKS, ALL_SUITS):
            if rank_.isnumeric():
                continue

            card = '{rank}_of_{suit}'.format(rank=rank_.upper(), suit=suit_)
            with self.assertRaises(ValueError):
                rank(card)

    def test_complete(self):
        ranks = {}
        for card in ALL_CARDS:
            rank_ = rank(card)
            ranks[rank_] = ranks.get(rank_, 0) + 1

        self.assertEqual(ranks, {
            'Ace': 4,
            '2': 4,
            '3': 4,
            '4': 4,
            '5': 4,
            '6': 4,
            '7': 4,
            '8': 4,
            '9': 4,
            '10': 4,
            'Jack': 4,
            'Queen': 4,
            'King': 4,
            'Joker': 2,
        })

    def test_reversable(self):
        for rank_, suit_ in itertools.product(ALL_RANKS, ALL_SUITS):
            card = '{rank}_of_{suit}'.format(rank=rank_, suit=suit_)
            self.assertEqual(rank(card), rank_)


class SuitsTestCase(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(suit('Ace_of_Spades'), 'Spades')

    def test_jokers(self):
        self.assertEqual(suit('Red_Joker'), 'Joker')
        self.assertEqual(suit('Black_Joker'), 'Joker')

    def test_invalid_suit(self):
        with self.assertRaises(ValueError):
            rank('11_of_Hearts')

    def test_flipped(self):
        for rank_, suit_ in itertools.product(ALL_RANKS, ALL_SUITS):
            card = '{suit}_of_{rank}'.format(rank=rank_, suit=suit_)
            with self.assertRaises(ValueError):
                suit(card)

    def test_capitalised(self):
        for rank_, suit_ in itertools.product(ALL_RANKS, ALL_SUITS):
            card = '{rank}_of_{suit}'.format(rank=rank_, suit=suit_.upper())
            with self.assertRaises(ValueError):
                suit(card)

    def test_complete(self):
        suits = {}
        for card in ALL_CARDS:
            suit_ = suit(card)
            suits[suit_] = suits.get(suit_, 0) + 1

        self.assertEqual(suits, {
            'Hearts': 13, 'Diamonds': 13,
            'Spades': 13, 'Clubs': 13,
            'Joker': 2,
        })

    def test_reversable(self):
        for rank_, suit_ in itertools.product(ALL_RANKS, ALL_SUITS):
            card = '{rank}_of_{suit}'.format(rank=rank_, suit=suit_)
            self.assertEqual(suit(card), suit_)
