import Benchmarking
from CustomAgents import *
from HeartsGame import HeartsGame
from PlayerAgents import *
from random import sample, shuffle

#   NOTES ABOUT MODIFYING THE CARD DECK:
#       Try not to make your max card below 13, since this stick the person with poggan with it far harder.
#       Try not to make your minimum card above 10, for game balance's sake.
#       Non-continuous ranges won't work without a full retool of the codebase.

#   PLACES TO MODIFY CODE IN ORDER TO MODIFY SIZE OF CARD DECK:
#       Line 51 of AgentBase. Change start card to new lowest card.
#       Line 57 of CardSet. Set range of cards.
#       Line 42 & 48 of HeartsGame. Change start card to new lowest card.
#       Line 117 of HeartsGame. Dealing is done in 1/4 swathes, and that number must be changed.
#       Line 155 & 156 of HeartsGame. Change Storslam value & threshold.

bot_names = ["Saxton", "Archimedes!", "Dell", "Elbert", "Rikoschett", "BeepBeepBoop", "HSRK", "Dane"]
shuffle(bot_names)
players = []
no_of_humans = int(input("How many humans are playing?"))
print("\n")

for i in range(0, no_of_humans):
    players.append(HumanOpponent(f"Human {i+1}"))
for i in range(0, 4-len(players)):
    players.append(SGAgentWithSendCardLogic(bot_names[i]))

for agent in players:
    print(f"{agent.name} | {agent.__class__.__name__}")

print("\n")
if no_of_humans > 0:
    mode = "Part-Auto"
else:
    mode = "Full-Auto"
hg = HeartsGame(*players, mode=mode)
hg.play_game(4, print=True)
