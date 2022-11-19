from AgentBaseClass import AgentBaseClass
from random import sample


class RandomAgent(AgentBaseClass):
    def __init__(self, name):
        super(RandomAgent, self).__init__(name)  # Calls AgentBaseClass __init__, making this function supplementary,
        # for stuff such as setting a memory variable.

    def pick_card(self, trick):
        return sample(self.get_legal_cards(trick).set, 1)[0]


class SimpleGoldfishAgent(AgentBaseClass):

    def __init__(self, name):
        super(SimpleGoldfishAgent, self).__init__(name)  # Calls AgentBaseClass __init__, making this function
        # supplementary, for stuff such as setting a memory variable.

    def pick_card(self, trick):
        if self.discard_mode(trick.get_suit()):
            return self.get_legal_cards(trick).set[0]
        else:
            if trick.get_trick_point_value() > 0:
                print("Trick worth more than nil!!!")
                if self.takeable(trick):
                    return self.hand.get_cards_of_suit(trick.get_suit(), reverse_sort=True).set[0]
            elif trick.get_suit() == "R" and trick.get_winning_card().value >= 10 and trick.get_cards_len == 3:
                pass

    def takeable(self, trick):
        trick_suit = trick.get_suit()
        if trick_suit == "Any":
            print("You're goin' first!")
            return True
        elif self.discard_mode(trick_suit) is True:
            print("Naaurr cahnt you strait up renons")
            return False
        else:
            highest_card_of_suit = self.hand.get_cards_of_suit(trick_suit, reverse_sort=True).set[0]
            if highest_card_of_suit.get_value() > trick.get_winning_card().get_value():
                print("GANKABLE BABY!")
                return True
            else:
                print("Skill issue: " + highest_card_of_suit.to_string())
                return False
