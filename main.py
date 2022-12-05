import Benchmarking
from HeartsGame import HeartsGame
from CustomAgents import *

players = [
    NyAgent("Temmie"),
    RandomAgent("DaVinki"),
    SimpleGoldfishAgent("Jambo"),
    SGAgentWithSendCardLogic("Peepo")
]

# HeartsGame(*players)
Benchmarking.benchmark(players, 100)
