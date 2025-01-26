import functools
import random
from .state import states, affordance, transition, k2ij
from .hint import Stone, State, Index, Coord


class Player:

    def __init__(self, stone: Stone):
        self.stone = stone
        self.state = None
        self.value = {state: 0. for state in states}
        self.alpha = 1e-2
        self.gamma = 1

    def top(self, ks: list[Index], ss: list[State]) -> list[Index]:
        vs = [self.value[s] for s in ss]
        mv = max(vs)
        ks_ = list()
        for k, v in zip(ks, vs):
            if v >= mv:
                ks_.append(k)
        return ks_

    def act(self, state: State) -> tuple[Stone, Coord]:
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
            reward + self.gamma * self.value[state] - self.value[self.state]
        )
        self.state = state
