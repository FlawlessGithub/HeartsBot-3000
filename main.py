import inspect
from HeartsGame import HeartsGame
from CustomAgents import *


players = [
    RandomAgent("Big Guy"),
    RandomAgent("Chicken Soup"),
    SimpleGoldfishAgent("Jambo"),
    RandomAgent("Schlatt")
]

HeartsGame(*players)
