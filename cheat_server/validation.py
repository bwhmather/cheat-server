from cheat_server.cards import ALL_CARDS, ALL_RANKS, ALL_SUITS

_undefined = object()


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


__all__ = [
    'validate_card',
    'validate_rank',
]
