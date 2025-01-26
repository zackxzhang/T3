from t3.state import Stone
from t3.reward import Victory, Survival
from t3.player import Player
from t3.game import Game


players = [
    Player(Stone.X, Victory),
    Player(Stone.O, Survival),
]

for _ in range(100):
    game = Game(players)
    while True:
        player = game.player
        action = player.act(game.state)
        signal = game.evo(action)
        for player in players:
            player.obs(signal, game.state)
        if game.winner:
            print('')
            print(game)
            break

for player in players:
    print('='*64)
    for s, v in player.value.items():
        if v != 0.:
            print(f"{s}: {v}")