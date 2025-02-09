import json
import random
from abc import ABC, abstractmethod
from enum import Flag
from math import inf
from .state import Stone, State, states, transitions, judge
from .value import Value
from .reward import Reward
from .optim import Schedule, ConstantSchedule
from .codec import (
    encode_stone, decode_stone,
    encode_state, decode_state,
    encode_value, decode_value,
    encode_reward, decode_reward,
)


class Mode(Flag):

    EXPLORE = 1
    EXPLOIT = 2


class Agent(ABC):

    def __init__(self, stone: Stone):
        self.stone = stone
        self.state: State

    @abstractmethod
    def eval(self):
        pass

    @abstractmethod
    def act(self, state: State) -> State:
        pass

    @abstractmethod
    def obs(self, winner: Stone, state: State):
        pass


class Amateur(Agent):

    def __init__(self, stone: Stone):
        super().__init__(stone)

    def eval(self):
        return self

    def act(self, state: State) -> State:
        actions = transitions(state, self.stone)
        action = random.choice(actions)
        return action

    def obs(self, winner: Stone, state: State):
        self.state = state


class Learner(Agent):

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
        self.mode: Mode

    def eval(self):
        self.alpha = ConstantSchedule(0.)
        self.epsilon = ConstantSchedule(0.)
        return self

    def save(self, file):
        data = {
            'stone': encode_stone(self.stone),
            'value': encode_value(self.value),
            'reward': encode_reward(self.reward),
        }
        with open(file, 'w') as f:
            json.dump(data, f)

    @classmethod
    def load(cls, file):
        with open(file, 'r') as f:
            data = json.load(f)
        stone = decode_stone(data['stone'])
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

    def obs(self, winner: Stone, state: State):
        match self.mode:
            case Mode.EXPLOIT:
                self.value[self.state] += self.alpha() * (
                    self.reward(winner) + self.gamma *
                    self.value[state] - self.value[self.state]
                )
            case _:
                pass
        self.state = state
