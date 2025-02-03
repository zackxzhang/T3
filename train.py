from t3.state import Stone, states, plot
from t3.value import init_value
from t3.reward import Victory, Survival
from t3.player import Amateur, Learner
from t3.game import Game
from t3.optim import CosineSchedule


m = 50_000
n = 80_000
wins = [0, 0, 0]

p1 = Learner(
    Stone.X, init_value(), Victory,
    alpha=CosineSchedule(m, 1e-2, 1e-4),
    epsilon=CosineSchedule(m, 0.40, 0.01),
)
p2 = Learner(
    Stone.O, init_value(), Victory,
    alpha=CosineSchedule(m, 1e-2, 1e-4),
    epsilon=CosineSchedule(m, 0.40, 0.01),
)
players = (p1, p2)


for _ in range(n):
    game = Game(players)
    while True:
        player = game.player
        action = player.act(game.state)
        winner = game.evo(action)
        if winner:
            for player in players:
                player.obs(winner, game.state)
            if winner == Stone.X:
                wins[1] += 1
            elif winner == Stone.O:
                wins[2] += 1
            else:
                wins[0] += 1
            break
        else:
            player.obs(winner, game.state)

print(f'X {wins[1]/n}')
print(f'- {wins[0]/n}')
print(f'O {wins[2]/n}')
print('-' * 8)


for player in players:
    print('-' * 32)
    states_ = sorted(states, key=player.value.__getitem__)
    for s in states_[:8] + states_[-8:]:
        print(plot(s))
        print(player.value[s])

p1.save('p1.json')
p2.save('p2.json')
