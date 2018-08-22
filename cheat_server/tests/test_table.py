import unittest
import random

from cheat_server.cards import ALL_CARDS
from cheat_server.table import Stack, Table


class StackTestCase(unittest.TestCase):

    def test_add_everything(self):
        stack = Stack(ALL_CARDS)
        self.assertEqual(set(stack), ALL_CARDS)

    def test_duplicates(self):
        cards = ['Ace_of_Spades', *ALL_CARDS]
        with self.assertRaises(ValueError):
            Stack(cards)

    def test_default(self):
        self.assertEqual(list(Stack()), [])

    def test_empty(self):
        self.assertEqual(list(Stack([])), [])

    def test_add_existing(self):
        stack = Stack(ALL_CARDS)
        with self.assertRaises(ValueError):
            stack.add(['Queen_of_Hearts'])


class TableTestCase(unittest.TestCase):

    def test_deal(self):
        # Deal out all of the cards.
        cards = list(ALL_CARDS)
        random.shuffle(cards)
        table = Table.deal(cards)

        # Check that deal didn't consume the list.
        self.assertEqual(set(cards), ALL_CARDS)

        # Check that the cards were dealt to each player in alternating order.
        hand_a, hand_b = table.hands
        for index, card in enumerate(cards):
            if index % 2:
                self.assertIn(card, hand_a)
            else:
                self.assertIn(card, hand_b)

        # Check that `played` and `discarded` stacks are empty.
        self.assertEqual(table.played, Stack())
        self.assertEqual(table.discarded, Stack())

    def test_play(self):
        # Set up the table.
        cards = list(ALL_CARDS)
        random.shuffle(cards)

        hands = [cards[0:12], cards[12:24]]
        played = cards[24:42]
        discarded = cards[42:]

        table = Table(
            hands=[Stack(hand) for hand in hands],
            played=Stack(played),
            discarded=Stack(discarded),
        )

        # Pick 4 random cards from the first player's hand and attempt to move
        # them to the played stack.
        move_1 = random.sample(list(table.hands[0]), 4)
        table = table.play(player=0, cards=move_1)

        # Check that the cards have actually been moved.
        self.assertEqual(set(table.hands[0]), set(hands[0]) - set(move_1))
        self.assertEqual(table.played, Stack(played + move_1))

    def test_fold(self):
        # Set up the table.
        cards = list(ALL_CARDS)
        random.shuffle(cards)

        hands = [cards[0:8], cards[8:16]]
        played = cards[16:24]
        discarded = cards[24:]

        table = Table(
            hands=[Stack(hand) for hand in hands],
            played=Stack(played),
            discarded=Stack(discarded),
        )

        # Fold.
        table = table.fold()

        # Check that the cards have actually been moved.
        self.assertEqual(table.played, Stack())
        self.assertEqual(table.discarded, Stack(discarded + played))

    def test_collect(self):
        # Set up the table.
        cards = list(ALL_CARDS)
        random.shuffle(cards)

        hands = [cards[0:16], cards[16:18]]
        played = cards[18:48]
        discarded = cards[48:]

        table = Table(
            hands=[Stack(hand) for hand in hands],
            played=Stack(played),
            discarded=Stack(discarded),
        )

        # Force the unfortunate second player to pick up the stack.
        table = table.collect(player=1)

        # Check that the cards have actually been moved.
        self.assertEqual(table.played, Stack())
        self.assertEqual(table.hands[1], Stack(hands[1] + played))
