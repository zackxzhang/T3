from t3.player import Player
from t3.arena import Arena
from t3.state import state_0
from t3.reward import victory, survival


players = [
    Player('x', state_0, victory),
    Player('o', state_0, survival),
]

for _ in range(1_000):
    arena = Arena([player.reward for player in players])
    state = arena.state
    rewards = (0, 0)
    while True:
        player = players[arena.round % 2]
        action = player.act(state)
        state, rewards = arena.evo(action)
        for player, reward in zip(players, rewards):
            player.obs(state, reward)
        if arena.ended:
            print(arena)
            break

for player in players:
    print('='*64)
    for s, v in player.value.items():
        if v != 0.:
            print(f"{s}: {v}")