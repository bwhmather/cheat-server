import unittest

from cheat_server.tests import test_cards
from cheat_server.tests import test_stack
from cheat_server.tests import test_table


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_cards),
    loader.loadTestsFromModule(test_stack),
    loader.loadTestsFromModule(test_table),
))
