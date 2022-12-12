from CardSet import Card, CardSet, ProbabilityCardSet


def rel_to_abs_plr_order(pos, start_pos):
    absolute = pos + start_pos
    if absolute > 3:
        absolute -= 4
    return absolute

class BlackBoxAgent2:
    def __init__(self, **kwargs):
        # self.ap = abs_pos
        self.name = kwargs.get("name", "")
        self.hand = ProbabilityCardSet(kwargs.get("initial_probabilities", 0.33))  # Dictionary of cards by likelihood*
        # of presence in the hand.
        self.played_cards = CardSet()
        self.value_cards = CardSet()
        self.renons = {
            "H": False,
            "S": False,
            "R": False,
            "K": False
        }

    def __hash__(self):
        return ord(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def renons_checks(self):
        for suit in self.renons:
            self.hand.mod_all_of_suit(suit, lambda p: p * self.renons[suit])

    def add_value_cards(self, value_card):
        if type(value_card) != list:
            value_card = [value_card]
        self.value_cards.add_cards(value_card)

    def mod_cards_of_suit(self, s, lambda_function, **kwarg):
        self.mod_cards(self.hand.get_cards_of_suit(s), lambda_function)

    def mod_cards(self, arr, lambda_function):
        if type(arr) != list:
            arr = [arr]
        self.hand.mod_cards(arr, lambda_function)


def filter_out_certains_from_probs(pcs):
    return_arr = []
    for c in pcs.probabilities:
        if 0.0 < pcs.probabilities[c] < 1.0:
            return_arr.append(c)
        else:
            pass
    return return_arr

def apply_func_if_uncertain(probabilities, lambda_function):
    for p in probabilities:
        if 0.0 < probabilities[p] < 1.0:
            p = probabilities[p]
        else:
            p = lambda_function(probabilities[p])
    return probabilities



class SecondMemory:
    def __init__(self, bound_player):
        self.owner = bound_player
        self.own_abs_pos = None
        self.players = []
        self.played_cards = CardSet()
        self.renons_amounts = {"H": 0, "S": 0, "R": 0, "K": 0}

    def create_black_boxes(self, players):
        for plr in players:
            if plr == self.owner:
                ip = 0.0
            else:
                ip = 0.33
            self.players.append(BlackBoxAgent2(name=plr.name, initial_probabilities=ip))

    def mod_cards_for_all(self, arr, lambda_function, **kwarg):
        for plr in self.players:
            plr.mod_cards(arr, lambda_function)

    def log_sent_cards(self, target_index, cards):
        for i in range(4):
            n = 0.0 + (i == target_index)
            self.players[i].mod_cards(cards, lambda p: n)

    def log_trick(self, trick, self_pos):
        trick_cards = trick.get_cards()
        trick_suit = trick.get_s()
        for rp in range(4):
            ap = rel_to_abs_plr_order(rp, trick.initial_player)
            if trick_cards.set[rp].get_s() != trick_suit:
                self.players[ap].renons[trick_suit] = True
            else:
                self.players[ap].renons[trick_suit] = False
        winner = self.players[trick.determine_winner()]
        self.mod_cards_for_all(trick.get_cards().set, lambda p: 0.0)
        self.played_cards.add_cards(trick.get_cards().set)
        winner.add_value_cards(trick.get_value_cards())
        self.recalc_probabilities()

    def log_new_cards(self, arr):
        for plr in self.players:
            if plr == self.owner:
                plr.mod_cards(arr, lambda p: 1.0)
            else:
                plr.mod_cards(arr, lambda p: 0.0)

    def recalc_probabilities(self):
        self.calc_renons_amounts()
        for suit in self.renons_amounts:
            suit_renons_amount = self.renons_amounts[suit]
            n = 3-suit_renons_amount
            for plr in self.players:
                cards_to_mod = self.filter_out_certains_from_arr(plr.hand.get_cards_of_suit(suit))
                plr.mod_cards(cards_to_mod, lambda p: 1.0 / (3 - suit_renons_amount))

    def filter_out_certains_from_arr(self, arr):
        return_arr = []
        probs = self.players[0].hand.probabilities
        for c in arr:
            if 0.0 < probs[c] < 1.0:
                return_arr.append(c)
            else:
                pass
        return return_arr

    def calc_renons_amounts(self):
        for suit in self.renons_amounts:
            r = 0
            for plr in self.players:
                if plr != self.owner:
                    r += plr.renons[suit]
            self.renons_amounts[suit] = r
