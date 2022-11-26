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
        trick_s = trick.get_s()
        if trick_s == "Any":  # You're first up to bat, kid!
            return self.get_legal_cards(trick).set[0]
        else:
            r10 = self.hand.find_card("R", 10)
            winning_v = trick.get_winning_c().get_v()
            huv = self.hand.get_highest_of_suit_under_v(trick_s, winning_v)
            lav = self.hand.get_lowest_of_suit_above_v(trick_s, winning_v)
            if self.discard_mode(trick_s):
                return self.get_legal_cards(trick).set[0]
            else:
                point_v = trick.get_trick_point_value()
                if point_v > 0 and self.takeable(trick):
                    return self.hand.get_highest_of_suit(trick_s)
                elif r10 and point_v > -9 and trick_s == "R" and winning_v < 10 and trick.get_len() == 3:
                    return r10
                else:  # point value =< 0 and r10 is not playable
                    if huv:
                        return huv
                    else:
                        return lav

    def takeable(self, trick):
        trick_suit = trick.get_s()
        if trick_suit == "Any":
            return True
        elif self.discard_mode(trick_suit) is True:
            return False
        else:
            if self.hand.get_highest_of_suit(trick_suit).get_v() > trick.get_winning_c().get_v():
                return True
            else:
                return False
