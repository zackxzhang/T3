from t3.state import Stone, states, plot
from t3.value import init_value
from t3.reward import Victory, Survival
from t3.agent import Amateur, Learner
from t3.game import Game, Arbiter
from t3.optim import CosineSchedule


m = 500_000
n = 800_000


a1 = Learner(
    Stone.X, init_value(), Victory,
    alpha=CosineSchedule(m, 4e-2, 1e-3),
    epsilon=CosineSchedule(m, 0.50, 0.01),
)
a2 = Learner(
    Stone.O, init_value(), Victory,
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


for agent in agents:
    print('-' * 32)
    ss = sorted(states, key=agent.value.__getitem__)
    for s in ss[:8] + ss[-8:]:
        print(plot(s))
        print(agent.value[s])


a1.save('a1.json')
a2.save('a2.json')
