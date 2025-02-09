from .state import Stone, State
from .value import Value
from .reward import Reward, Victory, Rush, Survival


def encode_stone(stone: Stone) -> str:
    return str(stone)


def decode_stone(string: str) -> Stone:
    return Stone[string]


def encode_state(state: State) -> str:
    return ''.join(map(str, state))


def decode_state(string: str) -> State:
    return tuple(map(Stone.__getitem__, string))


def encode_value(value: Value) -> dict[str, float]:
    return {encode_state(s): v for s, v in value.items()}


def decode_value(json: dict[str, float]) -> Value:
    return Value({decode_state(s): v for s, v in json.items()})


def encode_reward(reward: Reward) -> str:
    return reward.name


def decode_reward(string: str) -> type[Reward]:
    match string:
        case 'victory':
            return Victory
        case 'rush':
            return Rush
        case 'survival':
            return Survival
        case _:
            raise ValueError(f'no reward named {string}')
