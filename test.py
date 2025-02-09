from t3 import Stone, Amateur, Learner, Game, Arbiter


a1 = Learner.load('a1.json').eval()
a2 = Learner.load('a2.json').eval()
a3 = Amateur(Stone.X)
a4 = Amateur(Stone.O)


matches = ((a3, a4), (a1, a4), (a3, a2), (a1, a2))
n = 10_000


def rollout(agents, arbiter):
    game = Game(agents)
    while True:
        agent  = game.agent
        action = agent.act(game.state)
        winner = game.evo(action)
        if winner:
            arbiter(winner)
            break


for agents in matches:
    arbiter = Arbiter()
    for _ in range(n):
        rollout(agents, arbiter)
    print(arbiter)
