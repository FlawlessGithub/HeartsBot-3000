from CardSet import CardSet


class Agent:
    def __init__(self, name):
        self.name = name
        self.hand = CardSet()
        self.value_cards = CardSet()
        self.points = 0
        self.memory = ''  # Dummy for now. Will be useful later.

    def reset_cards(self):
        self.hand.clear()
        self.value_cards.clear()

    def reset_all(self):
        self.__init__(self.name)

    def pick_card(self, trick_cards, **kwarg):
        k2 = self.hand.find_card("K", 2)
        if k2:
            print(self.name + " played " + k2.get_txt_form() + "!")
            return k2
        pickable = self.get_legal_cards(trick_cards)
        picked_card = pickable[0]  # Placeholder
        print(self.name + " played " + picked_card.get_txt_form() + "!")
        if kwarg.get("destructive", True):
            self.remove_from_hand([picked_card])
        return picked_card

    def send_cards(self, target):
        pass  # Target var is in case I want to add some targeting to this thing (e.g: buffer players etc...)
        sent_card_1 = self.hand.set[0]
        sent_card_2 = self.hand.set[1]
        send = [sent_card_1, sent_card_2]
        self.remove_from_hand(send)
        return send

    def log_trick(self, trick):  # Registers trick to memory (in the future)
        pass

    def get_hand(self):
        return self.hand

    def add_to_hand(self, arr):
        self.hand.add_cards(arr, resort=True)

    def remove_from_hand(self, arr):
        self.hand.remove_cards(arr, resort=True)

    def get_legal_cards(self, trick_cards):  # DO NOT MODIFY
        legal_cards = list()
        if len(trick_cards.cards.set) > 0:
            suit = trick_cards.get_suit()
            for card in self.hand.set:
                if card.get_suit() == suit:
                    legal_cards.append(card)
            if len(legal_cards) == 0:  # You have no self of the correct suit, meaning you can discard any card.
                legal_cards = self.hand.set
        else:  # You are the first player. You may start a trick as you please.
            legal_cards = self.hand.set
        return legal_cards
