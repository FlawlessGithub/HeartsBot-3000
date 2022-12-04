from CardSet import CardSet


class AgentBase:
    def __init__(self, name):
        self.name = name
        self.hand = CardSet()
        self.value_cards = CardSet()
        self.points = 0

    def reset_cards(self):
        self.hand.clear()
        self.value_cards.clear()

    def reset_all(self):
        self.__init__(self.name)

    def play_card(self, trick, **kwarg):
        k2 = self.hand.find_card("K", 2)
        if k2:
            picked_card = k2
        else:
            picked_card = self.pick_card(trick)
        if kwarg.get("print", True):
            print(self.name + " played " + picked_card.to_string() + "!")
        if kwarg.get("destructive", True):
            self.remove_from_hand([picked_card])
        return picked_card

    def pick_card(self, trick):
        """
        Override this function in order to make a custom agent.
        :param trick: The trick currently being played, in form of a TrickCards class.
        :return: A Card instance from the agent's hand.
        """
        pass
        return self.get_legal_cards(trick).set[0]  # Placeholder.

    def send_cards(self, target):
        # Target var is in case I want to add some targeting to this thing (e.g: buffer players etc...)
        send = self.pick_cards_to_send(target)
        self.remove_from_hand(send)
        return send

    def pick_cards_to_send(self, target):
        sent_card_1 = self.hand.set[0]
        sent_card_2 = self.hand.set[1]
        return [sent_card_1, sent_card_2]

    def log_trick(self, trick):  # Registers trick to memory (in the future)
        pass

    def get_hand(self):
        return self.hand

    def add_to_hand(self, arr):
        self.hand.add_cards(arr, resort=True)

    def remove_from_hand(self, arr):
        self.hand.remove_cards(arr, resort=True)

    def is_renons(self, s):
        if self.hand.get_cards_of_suit(s).size <= 0:
            return True
        else:
            return False

    def get_legal_cards(self, trick):  # DO NOT MODIFY
        legal_cards = CardSet()
        if len(trick.cards.set) > 0:
            suit = trick.get_s()
            for card in self.hand.set:
                if card.get_s() == suit:
                    legal_cards.add_cards([card])
            if legal_cards.size == 0:  # You have no self of the correct suit, meaning you can discard any card.
                legal_cards.add_cards(self.hand.set)
        else:  # You are the first player. You may start a trick as you please.
            legal_cards.add_cards(self.hand.set)
        return legal_cards

    def discard_mode(self, trick_suit):
        if self.hand.get_cards_of_suit(trick_suit).size == 0 and trick_suit != "Any":
            return True
        else:
            return False
