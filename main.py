import inspect
from HeartsGame import HeartsGame
from CustomAgents import *


players = [
    RandomAgent("Big Guy"),
    RandomAgent("Chicken Soup"),
    PointComparerAgent("Jambo",""),
    RandomAgent("Schlatt")
]

HeartsGame(*players)
