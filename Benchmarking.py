import time

from HeartsGame import HeartsGame


class PlayerStats:
    def __init__(self, agent):
        self.agent_type = agent.__class__.__name__
        self.average_score = 0
        self.total_score = 0


def benchmark(players, trials):
    pd = {p: PlayerStats(p) for p in players}
    game_time = time.time()
    hg = HeartsGame(*players)
    for t in range(trials):
        hg.reset_cards()
        hg.reset_points()
        hg.play_game(4, print=False)
        i = 0
        for p in pd:
            pd[p].total_score += p.points
    game_time = time.time() - game_time
    for p in pd:
        pd[p].average_score = pd[p].total_score / trials
    print("Results from " + str(trials) + " games, played in " + str(game_time) + " seconds.")
    print("(That's " + str(trials / game_time) + " games a second.)\n")
    i = 0
    for p in sorted(pd, key=lambda p: pd[p].average_score, reverse=True):
        i += 1
        print("#" + str(i) + ": \"" + p.name + "\" | " + pd[p].agent_type)
        print("     avg. Score: " + str(pd[p].average_score))
        print("     total Score: " + str(pd[p].total_score))
