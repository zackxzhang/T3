import json
import random
from abc import ABC, abstractmethod
from .struct import Stone, State, Value, Mode
from .state import states, transitions, judge
from .reward import Reward, decode_reward
from .value import encode_value, decode_value
from .optim import Schedule, ConstantSchedule


class Player(ABC):

    def __init__(self, stone: Stone, *args, **kwargs):
        self.stone = stone
        self.state: State
        self.mode: Mode
        self.alpha: Schedule
        self.epsilon: Schedule

    def eval(self):
        self.alpha = ConstantSchedule(0.)
        self.epsilon = ConstantSchedule(0.)
        return self

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
        if random.uniform(0, 1) < self.epsilon():
            self.mode = Mode.EXPLORE
            action = random.choice(actions)
        else:
            self.mode = Mode.EXPLOIT
            actions = self.top(actions)
            if len(actions) == 1:
                action = actions[0]
            else:
                action = random.choice(actions)
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
