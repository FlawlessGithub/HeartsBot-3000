import Benchmarking
from CustomAgents import *
from HeartsGame import HeartsGame
from PlayerAgents import *

players = [
    SGAgentWithSendCardLogic("Temmie"),
    RandomAgent("DaVinki"),
    RandomAgent("Jambo"),
    RandomAgent("Peepo")
]

for player in players:
    if player.type == "Opponent":
        player.opponents = players
'''
hg = HeartsGame(*players, mode="Part-Auto")
hg.play_game(4, print=True)
'''

Benchmarking.benchmark(players, 1000)