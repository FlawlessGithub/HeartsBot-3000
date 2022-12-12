from AgentBase import AgentBase
from CardSet import Card, str_to_card


def card_sent_helper(c):
    if c == "?":
        return Card("?", 0)
    else:
        return str_to_card(c)


class HumanOpponent(AgentBase):
    def __init__(self, name):
        super(HumanOpponent, self).__init__(name)
        self.type = "Opponent"

    def play_card(self, trick, **kwarg):
        return str_to_card(input("What card did " + self.name + " play?"))

    def send_cards(self, target):
        print("What cards did " + self.name + " send to " + self.opponents[target].name + "?")
        return {card_sent_helper(string) for string in [input("Card 1: "), input("Card 2: ")]}


class ManualAgent(AgentBase):
    # WIP
    def __init__(self, name):
        super(AgentBase, self).__init__(name)
        self.type = "Manual"
