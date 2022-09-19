import random


class CardDeck:
    '''
    A glorified list class. Has functions for picking random cards, and shuffling. Generates full 52-card list on
    __init__ in H => S => R => K order.
    '''

    def __init__(self):
        self.deck = []
        for s in ["H", "S", "R", "K"]:
            for v in range(2, 15):
                self.deck.append((s, v))

    def print_card_list(self, **lst):
        '''

        :param lst: Kwarg specifying which array of cards to pretty-print. Defaults to the deck stored in the class.
        :return: N/A
        '''
        l = lst.get("lst", self.deck)
        for c in l:
            print(c[0] + str(c[1]), end="  ")
        print()  # Blank line after card list

    def shuffle(self):
        '''
        Shuffles the deck fully randomly by swapping cards around
        :return:
        '''
        dl = len(self.deck)
        print(dl)
        for i in range(dl):
            rand_index = random.randint(0, dl - 1)
            rand_card = self.deck[rand_index]
            self.deck[rand_index] = self.deck[i]
            self.deck[i] = rand_card

    def pick_rand(self, n, **destructive):
        '''
        :param n: The amount of cards to pick.
        :param destructive: Whether to remove the cards picked from the deck or not.
        :return: Array of random cards.
        '''
        d = destructive.get("destructive", True)
        picked = random.choices(self.deck, k=n)
        if d:
            self.remove_cards(picked)
        return picked

    def remove_cards(self, arr):
        for card in arr:
            try:
                self.deck.remove(card)
            except ValueError:
                print(card[0] + str(card[1]) + " is not in the deck!")


#   CLASS DEMO
cd = CardDeck()
print("unshuffled:")
cd.print_card_list()
print("shuffled:")
cd.shuffle()
cd.print_card_list()
print("\n\nlength of deck: " + str(len(cd.deck)))
print("3 random cards:")
cd.print_card_list(lst=cd.pick_rand(3))
print("length of deck: " + str(len(cd.deck)))

print("\n\nlength of deck: " + str(len(cd.deck)))
print("3 random cards:")
cd.print_card_list(lst=cd.pick_rand(3, destructive=False))
print("length of deck: " + str(len(cd.deck)))
