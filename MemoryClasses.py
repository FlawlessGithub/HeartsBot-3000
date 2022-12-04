from CardSet import CardSet


def n_to_pn(n, initial_p):
    pn = n + initial_p
    if pn > 3:
        pn -= 4
    return pn


class FirstMemory:
    def __init__(self):
        self.players = {}

    def log_trick(self, agent_pos, trick):
        for n in range(0, trick.get_len()):
            pn = n_to_pn(n, trick.initial_player)
            played_card = trick.get_cards().set[n]
            if pn not in self.players:
                self.players[pn] = BlackBoxAgent()  # Adding a breakpoint here breaks the code???
            self.players[pn].played_cards.add_cards([played_card])  # Adding a breakpoint here breaks the code???


class BlackBoxAgent:
    def __init__(self):
        self.played_cards = CardSet()
        self.value_cards = CardSet()
        self.renons = list()
