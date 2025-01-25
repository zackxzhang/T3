import functools
import random
from .state import states, affordance, transition, k2ij
from .hint import State


class Player:

    def __init__(self, stone, state, reward):
        self.stone = stone
        self.state = state
        self.reward = functools.partial(reward, stone)
        self.value = {state: 0. for state in states}
        self.alpha = 1e-2

    def top(self, ks, ss):
        vs = [self.value[s] for s in ss]
        mv = max(vs)
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
            ks = self.top(ks, ss)
            if len(ks) == 1:
                k = ks[0]
            else:
                k = random.choice(ks)
        return self.stone, k2ij(k)

    def obs(self, state, reward):
        # print(f"{self.state} -> {state}")
        self.value[self.state] += self.alpha * (
            reward + self.value[state] - self.value[self.state]
        )
        self.state = state
