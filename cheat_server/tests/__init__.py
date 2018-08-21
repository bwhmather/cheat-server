import unittest

from cheat_server.tests import test_cards


loader = unittest.TestLoader()
suite = unittest.TestSuite((
    loader.loadTestsFromModule(test_cards),
))
