import functools
import random
from .state import states, state_0, transitions, judge
from .hint import Stone, State
from .reward import Reward


class Player:

    def __init__(self, stone: Stone, reward: type[Reward]):
        self.stone = stone
        self.reward = reward(stone)
        self.state = state_0
        self.value = {state: 0. for state in states}
        self.alpha = 1e-2
        self.gamma = 1

    def top(self, actions: list[State]) -> list[State]:
        rewards = [self.reward(judge(a)) for a in actions]
        values = [self.value[a] for a in actions]
        bar = max(r + self.gamma * v for r, v in zip(rewards, values))
        return [
            a for a, r, v in zip(actions, rewards, values)
            if r + self.gamma * v >= bar
        ]

    def act(self, state: State) -> State:
        actions = transitions(state, self.stone)
        if random.uniform(0, 1) < 0.2:
            action = random.choice(actions)
        else:
            actions = self.top(actions)
            if len(actions) == 1:
                action = actions[0]
            else:
                action = random.choice(actions)
        return action

    def obs(self, winner: Stone, state: State):
        self.value[self.state] += self.alpha * (
            self.reward(winner) + self.gamma *
            self.value[state] - self.value[self.state]
        )
        self.state = state
