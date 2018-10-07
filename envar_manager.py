import os


STATE = "FROG_STATE"
DIRECTIONS = "FROG_DIRECTIONS"


def is_state(_state):
    return os.environ[STATE] == _state


def set_state(_state):
    os.environ[STATE] = _state


def get_directions():
    return [d for d in os.environ[DIRECTIONS].split(",") if d]


def set_directions(_directions):
    os.environ[DIRECTIONS] = ",".join(_directions)
    print("directions:", get_directions())


def add_direction(_direction):
    set_directions(get_directions() + [_direction])
