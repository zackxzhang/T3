import functools
import json
import random
from abc import ABC, abstractmethod
from .struct import Stone, State, Value
from .state import states, transitions, judge
from .reward import Reward, decode_reward
from .value import make_value, encode_value, decode_value


class Player(ABC):

    def __init__(self, stone: Stone, *args, **kwargs):
        self.stone = stone
        self.state: State

    @abstractmethod
    def act(self, state: State) -> State:
        ...

    @abstractmethod
    def obs(self, winner: Stone, state: State):
        ...


class Amateur(Player):

    def __init__(self, stone: Stone):
        super().__init__(stone)

    def act(self, state: State) -> State:
        actions = transitions(state, self.stone)
        action = random.choice(actions)
        return action

    def obs(self, winner: Stone, state: State):
        self.state = state


class Learner(Player):

    def __init__(
        self,
        stone: Stone,
        reward: type[Reward],
        value: Value | None = None,
    ):
        super().__init__(stone)
        self.reward = reward(stone)
        self.value = value if value else make_value()
        self.alpha = 1e-2
        self.gamma = 1

    def save(self, file):
        data = {
            'stone': str(self.stone),
            'reward': self.reward.name,
            'value': encode_value(self.value),
        }
        with open(file, 'w') as f:
            json.dump(data, f)

    @classmethod
    def load(cls, file):
        with open(file, 'r') as f:
            data = json.load(f)
        stone = Stone[data['stone']]
        reward = decode_reward(data['reward'])(stone)
        value = decode_value(data['value'])
        return cls(stone, reward, value)

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
