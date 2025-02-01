from t3.state import Stone, states, plot
from t3.reward import Victory, Survival
from t3.player import Amateur, Learner
from t3.game import Game


players = (
    Amateur(Stone.X),
    Amateur(Stone.O),
)

n = 10_000
wins = {Stone.X: 0, Stone.O: 0, Stone.X | Stone.O: 0}
for _ in range(n):
    game = Game(players)
    while True:
        player = game.player
        action = player.act(game.state)
        winner = game.evo(action)
        if winner:
            wins[winner] += 1
            break
print('win ratio\n=========')
print(f'X:  {wins[Stone.X]/n}')
print(f'O:  {wins[Stone.O]/n}')
print(f'XO: {wins[Stone.X | Stone.O]/n}')
