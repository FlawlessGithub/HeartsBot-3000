import Benchmarking
from CustomAgents import *
from HeartsGame import HeartsGame
from PlayerAgents import *

players = [
    SGAgentWithSendCardLogic("Bot 1"),
    RandomAgent("Bot 2"),
    RandomAgent("Bot 3"),
    RandomAgent("Archimedes!")
]



Benchmarking.benchmark(players, 10000)

