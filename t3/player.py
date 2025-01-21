import functools
import random
from .state import states, affordance, transition, k2ij
from .hint import State


class Player:

    def __init__(self, stone, reward):
        self.stone = stone
        self.reward = functools.partial(reward, stone)
        self.value = {state: 0. for state in states}

    def top(self, ks, ss):
        vs = [self.value[s] for s in ss]
        mv = max(values)
        out = list()
        for k, v in zip(ks, vs):
            if v >= mv:
                out.append(k)
        return out

    def act(self, state: State) -> tuple[str, tuple[int, int]]:
        ks = [k for k in affordance(state)]
        if random.uniform(0, 1) < 0.2:
            k = random.choice(ks)
        else:
            ss = [transition(state, k, self.stone) for k in ks]
            ss = self.top(ks, ss)
            if len(ss) == 1:
                s = ss[0]
            else:
                s = random.choice(ss)
        return self.stone, k2ij(k)


    def obs(self, state, reward):
        # temporal difference
        pass
