import unittest

from cheat_server.cards import ALL_CARDS
from cheat_server.table import Stack


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
