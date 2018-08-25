import unittest
import secrets

from cheat_server import shuffle


class ShuffleTestCase(unittest.TestCase):
    def test_seed_deterministic(self):
        seed = secrets.randbits(2048)

        state_a = shuffle.seed_state(seed)
        state_b = shuffle.seed_state(seed)

        self.assertEqual(state_a, state_b)

    def test_sample_updates_state(self):
        seed = secrets.randbits(2048)
        state_a = shuffle.seed_state(seed)

        value_a, state_b = shuffle.sample(state_a)
        value_b, state_c = shuffle.sample(state_b)

        self.assertNotEqual(state_a, state_b)
        self.assertNotEqual(state_b, state_c)
        self.assertNotEqual(value_a, value_b)

    def test_shuffle_updates_state(self):
        seed = secrets.randbits(2048)
        input_state = shuffle.seed_state(seed)
        input_array = list(range(100))

        output_array, output_state = shuffle.shuffle(input_array, input_state)

        self.assertEqual(set(input_array), set(output_array))
        self.assertNotEqual(input_array, output_array)
        self.assertNotEqual(input_state, output_state)

    def test_depends_on_seed(self):
        seed_a = secrets.randbits(2048)
        seed_b = secrets.randbits(2048)
        assert seed_a != seed_b

        input_array = list(range(100))

        state_a = shuffle.seed_state(seed_a)
        state_b = shuffle.seed_state(seed_b)

        output_array_a, _ = shuffle.shuffle(input_array, state_a)
        output_array_b, _ = shuffle.shuffle(input_array, state_b)

        self.assertNotEqual(output_array_a, output_array_b)
