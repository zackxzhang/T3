import threading
from .state import states, encode_state, decode_state


class Value(dict):

    def __init__(self, *args, k=4, **kwargs):
        self.k = k
        self.loc = threading.Lock()
        self.sem = threading.Semaphore(k)
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        with self.loc:
            pass
        self.sem.acquire()
        try:
            return super().__getitem__(key)
        finally:
            self.sem.release()

    def __setitem__(self, key, value):
        with self.loc:
            for _ in range(self.k):
                self.sem.acquire()
        try:
            super().__setitem__(key, value)
        finally:
            for _ in range(self.k):
                self.sem.release()

    def items(self):
        with self.loc:
            return super().items()


def init_value(constant: float = 0., random: bool = False) -> Value:
    return Value((state, constant) for state in states)


def encode_value(value: Value) -> dict[str, float]:
    return {encode_state(s): v for s, v in value.items()}


def decode_value(json: dict[str, float]) -> Value:
    return Value((decode_state(s), v) for s, v in json.items())