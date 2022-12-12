import Benchmarking
from CustomAgents import *
from HeartsGame import HeartsGame
from PlayerAgents import *

players = [
    SGAgentWithSendCardLogic("Temmie"),
    NyAgent("DaVinki"),
    RandomAgent("Jambo"),
    RandomAgent("Peepo")
]


hg = HeartsGame(*players, mode="Full-Auto")
hg.play_game(4, print=True)

