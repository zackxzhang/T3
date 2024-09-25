from .state import states, stringify


class Player:

    def __init__(self):
        self.value = {state: 0 for state in states}

    def act(self, state):
        ...
        # exploitation
        # exploration

    def obs(self, reward):
        ...
         # dp? mc? td?