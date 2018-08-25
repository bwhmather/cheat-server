import random

from validation import validate_list


def seed_state(seed=None):
    # TODO implement an internal random number generator to guarantee
    # determinism.
    rng = random.Random(seed)
    state = rng.getstate()
    return state


def sample(state):
    """
    Extracts the next 64 bit integer from the current state and returns it and
    the next state.
    """
    # TODO implement an internal random number generator to guarantee
    # determinism.
    rng = random.Random()
    rng.setstate(state)
    value = rng.randrange((2**64) - 1)
    state = rng.getstate()
    return value, state


def shuffle(array, state):
    validate_list(array)

    # Sequentially produce a random weight for each value in the array.
    weights = []
    for _ in array:
        weight, state = sample(state)
        weights.append(weight)

    # Sort the array, using the weight stored in the weights array as key.
    shuffled = [
        value
        for _, value in sorted(
            enumerate(array),
            key=lambda pair: weights[pair[0]],
        )
    ]

    return shuffled, state
