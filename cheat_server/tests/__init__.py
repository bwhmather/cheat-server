import unittest

from cheat_server.tests import test_cards
from cheat_server.tests import test_table


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_cards),
    loader.loadTestsFromModule(test_table),
))
