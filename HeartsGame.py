from CardSet import CardSet


class HeartsGame:
    def __init__(self, *agents):
        self.deck = CardSet(populate=True)
        self.played_cards = CardSet()
        self.agents = list(agents)
        self.play_game(1)

    def play_game(self, rounds):
        for r in range(rounds):
            self.play_round(r)
            print("\nPOINTS:")
            for agent in self.agents:
                print(agent.name + ": " + str(agent.points))
        print("Game over!\n")
        ranked = sorted(self.agents, key=lambda a: a.points, reverse=True)
        print("FINAL STANDINGS:")
        for agent in ranked:
            print(agent.name + ": " + str(agent.points) + " points")
        winner = ranked[0]
        print("The winner, with " + str(winner.points) + " points, is " + winner.name + "!")
        print("Total points: " + str(sum([a.points for a in self.agents])))

    def play_round(self, round_number):
        self.deal(self.agents)
        self.players_send_cards(round_number)
        for agent in self.agents:
            if agent.get_hand().find_card("K", 2):
                starting_agent = agent
                print("Starting agent is: " + starting_agent.name)

        for x in range(0, 13):  # Play all the tricks
            starting_agent = self.play_trick(starting_agent, rn=round_number + 1, tn=x + 1)
        for agent in self.agents:
            agent.points += tally_points(agent.value_cards)
        self.reset_cards()
        return

    def play_trick(self, starting_agent, **kwargs):
        print("---------------------------------\nROUND " + str(kwargs.get("rn", 1)) + " | TRICK " + str(
            kwargs.get("tn", 1)) + "\n")
        start_index = self.agents.index(starting_agent)
        trick = TrickCards(start_index)
        agent_iter = self.agents[start_index:] + self.agents[:start_index]  # Loops around the players
        # instead of cutting off after index 3
        for agent in agent_iter:
            pc = agent.play_card(trick)
            self.played_cards.add_cards([pc])
            trick.add_card(pc)  # The trick is modified by the player, who is motivating
            # their decision by taking the trick (so far) as input.
        winner = agent_iter[trick.determine_winner()]
        winner.value_cards.add_cards(trick.get_value_cards())
        print(winner.name + " wins the trick.")
        for agent in agent_iter:
            agent.log_trick(trick)
        return winner  # next starting_agent

    def players_send_cards(self, round_number):
        match round_number:
            case 0:
                target_mod = +1
            case 1:
                target_mod = -1
            case 2:
                target_mod = +2
            case _:
                return  # No-send round
        sent = {}  # target: cards
        for i in range(len(self.agents)):
            j = i + target_mod
            if j > 3:
                j -= 4
            if j < 0:
                j += 4
            sc = self.agents[i].send_cards(j)
            sent[self.agents[j]] = sc
            print(self.agents[i].name + " sent: ", end="")
            for c in sc:
                print(c.to_string(), end=" ")
            print("to " + self.agents[j].name)
        for target in sent:
            target.add_to_hand(sent[target])

    def deal(self, targets):
        for target in targets:
            target.add_to_hand(self.deck.pick_rand(n=13, destructive=True))

    def reset_cards(self):
        for agent in self.agents:
            agent.reset_cards()
        self.deck.clear()
        self.deck.generate_full_deck()
        self.played_cards.clear()


def tally_points(cards, **clean_tables):
    p = 0
    if len(cards.set) == 0 and clean_tables.get("clean_tables", True):
        return 0 # 5  # Clean table
    elif len(cards.set) == 15:
        return 26
    else:
        for card in cards.set:
            if card.get_s() == "H":
                p -= 1
            elif card.get_s() == "S":
                if card.get_v() == 12:
                    p -= 13
            elif card.get_s() == "R" and card.get_v() == 10:
                p += 10
    return p


class TrickCards:
    def __init__(self, p1):
        self.initial_player = p1
        self.cards = CardSet()
        self.value_cards = CardSet()

    def get_s(self):
        if self.cards.size == 0:
            return "Any"
        return self.cards.set[0].get_s()

    def get_cards(self):
        return self.cards

    def get_len(self):
        return self.cards.size

    def get_value_cards(self):
        return self.value_cards.set

    def get_trick_point_value(self):
        return tally_points(self.value_cards, clean_tables=False)

    def add_card(self, card):
        self.cards.add_cards(arr=[card])
        if card.is_value_card():
            self.value_cards.add_cards([card])

    def determine_winner(self):
        winner = self.cards.set[0]
        for card in self.cards.set:
            if card.get_s() == winner.get_s():
                if card.get_v() > winner.get_v():
                    winner = card
        # print("This trick was worth "+str(self.get_trick_point_value())+" points.")
        return self.cards.set.index(winner)

    def get_winning_c(self):
        winner = self.cards.set[0]
        for card in self.cards.set:
            if card.get_s() == winner.get_s():
                if card.get_v() > winner.get_v():
                    winner = card
        return winner