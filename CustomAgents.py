from random import sample

from AgentBase import AgentBase
from MemoryClasses import SecondMemory


class RandomAgent(AgentBase):
    def __init__(self, name):
        super(RandomAgent, self).__init__(name)  # Calls AgentBaseClass __init__, making this function supplementary,
        # for stuff such as setting a memory variable.

    def send_cards(self, target):
        return sample(self.hand.set, 2)

    def pick_card(self, trick):
        return sample(self.get_legal_cards(trick).set, 1)[0]


class SimpleGoldfishAgent(AgentBase):

    def __init__(self, name):
        super(SimpleGoldfishAgent, self).__init__(name)  # Calls AgentBaseClass __init__, making this function
        # supplementary, for stuff such as setting a memory variable.

    def pick_card(self, trick):
        trick_s = trick.get_s()
        if trick_s == "?":  # You're first up to bat, kid!
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
                elif r10 and point_v > -9 and trick_s == "R" and winning_v < 10 and trick.get_pos() == 3:
                    return r10
                else:  # point value =< 0 and r10 is not playable
                    if huv:
                        return huv
                    else:
                        return lav

    def takeable(self, trick):
        trick_suit = trick.get_s()
        if trick_suit == "?":
            return True
        elif self.discard_mode(trick_suit) is True:
            return False
        else:
            if self.hand.get_highest_of_suit(trick_suit).get_v() > trick.get_winning_c().get_v():
                return True
            else:
                return False


class SGAgentWithSendCardLogic(SimpleGoldfishAgent):
    def __init__(self, name):
        super(SGAgentWithSendCardLogic, self).__init__(name)

    def pick_cards_to_send(self, target):
        s12 = self.hand.find_card("S", 12)
        hand_scores = {}
        for card in self.hand.set:
            c_score = 0
            match card.get_s():
                case "H":
                    if card.get_v() >= 7:
                        c_score += card.get_v() + self.hand.get_cards_of_suit_under_v("H", 7).size
                    else:
                        c_score += card.get_v() - self.hand.get_cards_of_suit_above_v("H", 6).size
                case "S":
                    if card.get_v() > 12:
                        c_score += 10 * 13 - self.hand.get_size_of_suit("S")
                    elif card.get_v() == 12:
                        if self.hand.get_cards_of_suit(
                                "S").size > 7:  # Nobody can burn through your "safe" spades at >7.
                            c_score += 0  # Just pawn it off on someone else
                        else:
                            c_score += (20 - self.hand.get_size_of_suit("S"))
                    else:
                        c_score += 0
                case "R":
                    if card.get_v() >= 10:
                        c_score += -100  # Taking R10 above all else
                    else:
                        c_score += 0
                case "K":
                    c_score += card.get_v() * 0.5
            hand_scores[card] = c_score
        c1 = max(hand_scores, key=hand_scores.get)
        del hand_scores[c1]
        c2 = max(hand_scores, key=hand_scores.get)
        return [c1, c2]


class NyAgent(AgentBase):
    def __init__(self, name):
        super(NyAgent, self).__init__(name)
        self.memory = SecondMemory(self)
        self.ap = None

    def pick_card(self, trick):
        self.ap = trick.get_pos()
        return self.get_legal_cards(trick).pick_rand(1)[0]

    def log_trick(self, trick):
        self.memory.log_trick(trick, self.ap)
