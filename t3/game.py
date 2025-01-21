from .player import Player
from .arena import Arena
from .reward import victory, survival


players = [
    Player('x', victory),
    Player('o', survival),
]

for _ in range(8):
    arena = Arena([player.reward for player in players])
    state = arena.state
    rewards = (0, 0)
    while True:
        player = players[arena.round % 2]
        action = player.act(state, rewards)
        state, rewards = arena.evo(action)
        for player, reward in (players, rewards):
            player.obs(state, reward)
        if arena.ended:
            break
