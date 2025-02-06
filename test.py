import multiprocessing as mp
from t3.state import Stone
from t3.player import Amateur, Learner
from t3.game import Game, Arbiter


p1 = Learner.load('p1.json').eval()
p2 = Learner.load('p2.json').eval()
p3 = Amateur(Stone.X)
p4 = Amateur(Stone.O)
matches = ((p3, p4), (p1, p4), (p3, p2), (p1, p2))
n = 10_000


def test(players, arbiter):
    game = Game(players)
    while True:
        player = game.player
        action = player.act(game.state)
        winner = game.evo(action)
        if winner:
            arbiter(winner)
            break


for players in matches:
    arbiter = Arbiter()
    for _ in range(n):
        game = Game(players)
        while True:
            player = game.player
            action = player.act(game.state)
            winner = game.evo(action)
            if winner:
                arbiter(winner)
                break
    print(arbiter)
