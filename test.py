from t3.state import Stone
from t3.player import Amateur, Learner
from t3.game import Game


p1 = Learner.load('p1.json').eval()
p2 = Learner.load('p2.json').eval()
p3 = Amateur(Stone.X)
p4 = Amateur(Stone.O)
matches = ((p3, p4), (p1, p4), (p3, p2), (p1, p2))
n = 10_000

for players in matches:
    wins = [0, 0, 0]
    for _ in range(n):
        game = Game(players)
        while True:
            player = game.player
            action = player.act(game.state)
            winner = game.evo(action)
            if winner == Stone.X | Stone.O:
                wins[0] += 1
            elif winner == Stone.X:
                wins[1] += 1
            elif winner == Stone.O:
                wins[2] += 1
            else:
                continue
            break
    print(f'X {wins[1]/n}')
    print(f'- {wins[0]/n}')
    print(f'O {wins[2]/n}')
    print('--------')
