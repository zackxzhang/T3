from .struct import Value
from .state import states, encode_state, decode_state


def init_value(constant=0., random=False):
    return {s: constant for s in states}


def encode_value(value: Value) -> dict[str, float]:
    return {encode_state(s): v for s, v in value.items()}


def decode_value(json: dict[str, float]) -> Value:
    return {decode_state(s): v for s, v in json.items()}
