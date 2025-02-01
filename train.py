from t3.state import Stone, states, plot
from t3.reward import Victory, Survival
from t3.player import Amateur, Learner
from t3.game import Game


players = (
    Learner(Stone.X, Victory),
    Learner(Stone.O, Survival),
)

for _ in range(100):
    game = Game(players)
    while True:
        player = game.player
        action = player.act(game.state)
        winner = game.evo(action)
        for player in players:
            player.obs(winner, game.state)
        if winner:
            print('')
            print(plot(game.state))
            break

for player in players:
    print('='*64)
    states_ = sorted(states, key=player.value.__getitem__)
    for s in states_[:10]:
        print('')
        print(f"{plot(s)} : {player.value[s]}")
    for s in states_[-10:]:
        print('')
        print(f"{plot(s)} : {player.value[s]}")


players[0].save('player.json')
print(type(Learner.load('player.json')))
