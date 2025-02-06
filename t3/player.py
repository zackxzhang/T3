import json
import random
from abc import ABC, abstractmethod
from math import inf
from .struct import Stone, State, Mode
from .state import states, transitions, judge
from .reward import Reward, decode_reward
from .value import Value, encode_value, decode_value
from .optim import Schedule, ConstantSchedule


class Player(ABC):

    def __init__(self, stone: Stone, *args, **kwargs):
        self.stone = stone
        self.mode: Mode
        self.alpha: Schedule
        self.epsilon: Schedule

    def eval(self):
        self.alpha = ConstantSchedule(0.)
        self.epsilon = ConstantSchedule(0.)
        return self

    @abstractmethod
    def act(self, state: State) -> State:
        pass

    @abstractmethod
    def obs(self, winner: Stone, state_a: State, state_b: State):
        pass


class Amateur(Player):

    def __init__(self, stone: Stone):
        super().__init__(stone)

    def act(self, state: State) -> State:
        actions = transitions(state, self.stone)
        action = random.choice(actions)
        return action

    def obs(self, winner: Stone, state_a: State, state_b: State):
        pass


class Learner(Player):

    def __init__(
        self,
        stone: Stone,
        value: Value,
        reward: type[Reward],
        alpha: Schedule = ConstantSchedule(1e-2),
        epsilon: Schedule = ConstantSchedule(0.2),
    ):
        super().__init__(stone)
        self.reward = reward(stone)
        self.value = value
        self.gamma = 1
        self.alpha = alpha
        self.epsilon = epsilon

    def save(self, file):
        data = {
            'stone': str(self.stone),
            'value': encode_value(self.value),
            'reward': self.reward.name,
        }
        with open(file, 'w') as f:
            json.dump(data, f)

    @classmethod
    def load(cls, file):
        with open(file, 'r') as f:
            data = json.load(f)
        stone = Stone[data['stone']]
        value = decode_value(data['value'])
        reward = decode_reward(data['reward'])
        return cls(stone, value, reward)

    def top(self, actions: list[State]) -> State:
        action_values = [
            (a, self.reward(judge(a)) + self.gamma * self.value[a])
            for a in actions
        ]
        random.shuffle(action_values)
        best = -inf
        for a, v in action_values:
            if v > best:
                best, action = v, a
        return action

    def act(self, state: State) -> State:
        actions = transitions(state, self.stone)
        if random.uniform(0, 1) < self.epsilon():
            self.mode = Mode.EXPLORE
            action = random.choice(actions)
        else:
            self.mode = Mode.EXPLOIT
            action = self.top(actions)
        return action

    def obs(self, winner: Stone, state_a: State, state_b: State):
        match self.mode:
            case Mode.EXPLOIT:
                self.value[state_a] += self.alpha() * (
                    self.reward(winner) + self.gamma *
                    self.value[state_b] - self.value[state_a]
                )
            case _:
                pass
