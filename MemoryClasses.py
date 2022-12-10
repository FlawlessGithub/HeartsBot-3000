from CardSet import CardSet, ProbabilityCardSet


def rel_to_abs_plr_order(pos, start_pos):
    abs = pos + start_pos
    if abs > 3:
        abs -= 4
    return abs


class SecondMemory:
    def __init__(self, bound_player):
        self.owner = bound_player
        self.own_abs_pos = None
        self.players = {}

    def compile_played_cards(self):
        pcs = CardSet()
        for player in self.players:
            pcs.add_cards(self.players[player].played_cards.set)

    def log_sent_cards(self, target_index, cards):
        self.players[target_index].add_to_hand(cards, 1.0)

    def log_trick(self, trick, self_pos):
        for n in range(4):
            pn = rel_to_abs_plr_order(n, trick.initial_player)
            played_card = trick.get_cards().set[n]
            if pn not in self.players:
                self.players[pn] = BlackBoxAgent2()  # Adding a breakpoint here breaks the code???
                if n == self_pos:
                    self.own_abs_pos = pn
                    self.players[pn] = self.owner
            if n == self_pos:
                self.own_abs_pos = pn
                self.players[pn] = self.owner
            if self.players[pn] != self.owner:
                self.players[pn].add_played_card(played_card, trick)  # Adding a breakpoint here breaks the code???


class BlackBoxAgent2:
    def __init__(self):
        # self.ap = abs_pos
        self.hand = ProbabilityCardSet()  # Dictionary of cards by likelihood* of presence in the hand. (*probability may have no bearing)
        self.played_cards = CardSet()
        self.value_cards = CardSet()
        self.renons = {
            "H": False,
            "S": False,
            "R": False,
            "K": False
        }

    def renons_check(self):
        for suit in self.renons:
            self.hand.mod_all_of_suit(suit, lambda p: p * self.renons[suit])

    def add_played_card(self, played_card, trick):
        self.played_cards.add_cards([played_card])
        self.renons[trick.get_s()] = played_card.get_s() != trick.get_s()
        self.renons_check()

    def add_to_hand(self, cards, probability):
        for card in cards:
            self.hand[card] = probability


'''
def n_to_pn(n, initial_p):
    pn = n + initial_p
    if pn > 3:
        pn -= 4
    return pn


class FirstMemory:
    def __init__(self):
        self.players = {}

    def log_trick(self, agent_pos, trick):
        for n in range(0, agent_pos):
            pn = n_to_pn(n, trick.initial_player)
            played_card = trick.get_cards().set[n]
            if pn not in self.players:
                self.players[pn] = BlackBoxAgent()  # Adding a breakpoint here breaks the code???
            self.players[pn].add_played_card(played_card, trick)  # Adding a breakpoint here breaks the code???

    def eval_trick(self, trick):
        pass


class BlackBoxAgent:
    def __init__(self):
        self.played_cards = CardSet()
        self.value_cards = CardSet()
        self.unlikely_cards = CardSet()
        self.not_cards = CardSet()
        self.renons = list()

    def add_played_card(self, card, trick):
        self.played_cards.add_cards([card])

    def eval_card(self, card):
        pass
'''
