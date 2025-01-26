from t3.state import Stone
from t3.reward import victory, survival
from t3.player import Player
from t3.game import Game


players = [
    Player(Stone.X),
    Player(Stone.O),
]
reward_functions = [
    victory(players[0]),
    survival(players[1]),
]

for _ in range(8):
    game = Game(players, reward_functions)
    while True:
        player = players[game.round % 2]
        action = player.act(game.state)
        rewards = game.evo(action)
        for player, reward in zip(players, rewards):
            player.obs(game.state, reward)
        if game.winner:
            print('')
            print(game)
            break

for player in players:
    print('='*64)
    for s, v in player.value.items():
        if v != 0.:
            print(f"{s}: {v}")