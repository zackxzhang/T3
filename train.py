from t3 import Stone, Value, Victory, Learner, Game, Arbiter, CosineSchedule


m = 500_000
n = 800_000


a1 = Learner(
    Stone.X, Value(), Victory,
    alpha=CosineSchedule(m, 4e-2, 1e-3),
    epsilon=CosineSchedule(m, 0.50, 0.01),
)
a2 = Learner(
    Stone.O, Value(), Victory,
    alpha=CosineSchedule(m, 4e-2, 1e-3),
    epsilon=CosineSchedule(m, 0.50, 0.01),
)


def rollout(agents, arbiter):
    game = Game(agents)
    while True:
        agent  = game.agent
        action = agent.act(game.state)
        winner = game.evo(action)
        if winner:
            for agent in agents:
                agent.obs(winner, game.state)
            arbiter(winner)
            break
        else:
            agent.obs(winner, game.state)


agents = (a1, a2)
arbiter = Arbiter()
for _ in range(n):
    rollout(agents, arbiter)
print(arbiter)
a1.save('a1.json')
a2.save('a2.json')
