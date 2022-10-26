import random


class CardSet:
    '''
    A glorified list class used both for the deck of cards and the players' hands. Has functions for picking random
    cards, and shuffling. Starts empty but can be populated with 52 cards using the generate_full_deck method.
    '''

    def __init__(self, **kwargs):
        self.deck = []
        if kwargs.get("populate", False):
            self.generate_full_deck()

    def generate_full_deck(self):
        '''
        Generates full 52-card list on in H => S => R => K order.
        :return:
        '''
        for s in ["H", "S", "R", "K"]:
            for v in range(2, 15):
                self.deck.append((s, v))

    def print_card_list(self, **kwargs):
        '''

        :param lst: Kwarg specifying which array of cards to pretty-print. Defaults to the deck stored in the class.
        :return: N/A
        '''
        l = kwargs.get("lst", self.deck)
        if len(l) == 0:
            print("No cards!", end="")
        else:
            for c in l:
                print(c[0] + str(c[1]), end=" ")
        print()  # Blank line after card list

    def shuffle(self):
        '''
        Shuffles the deck fully randomly by swapping cards around
        :return:
        '''
        dl = len(self.deck)
        for i in range(dl):
            rand_index = random.randint(0, dl - 1)
            rand_card = self.deck[rand_index]
            self.deck[rand_index] = self.deck[i]
            self.deck[i] = rand_card

    def sort(self):
        self.deck = sorted(self.deck, key=lambda x: self.sort_help_func(x))

    def sort_help_func(self, card):     # Makes it so that suits aren't sorted alphabetically, but in custom HSRK order.
        return card[1] + 13 * {"H": 1, "S": 2, "R": 3, "K": 4}[card[0]]

    def pick_rand(self, n, **kwargs):
        '''
        :param n: The amount of cards to pick.
        :param destructive: Whether to remove the cards picked from the deck or not.
        :return: Array of random cards.
        '''
        d = kwargs.get("destructive", True)
        picked = random.choices(self.deck, k=n)
        if d:
            self.remove_cards(picked)
        return picked

    def add_cards(self, arr, **kwargs):
        for card in arr:
            try:
                self.deck.append(card)
            except ValueError:
                print(card[0] + str(card[1]) + " is not in the deck!")
        if kwargs.get("resort", True):
            self.sort()

    def remove_cards(self, arr, **kwargs):
        for card in arr:
            try:
                self.deck.remove(card)
            except ValueError:
                print(card[0] + str(card[1]) + " is not in the deck!")
        if kwargs.get("resort", True):
            self.sort()


#   CLASS DEMO
cd = CardSet(populate=True)
print("unshuffled:")
cd.print_card_list()
print("shuffled:")
cd.shuffle()
cd.print_card_list()
print("sorted:")
cd.sort()
cd.print_card_list()


print("\n\nlength of deck: " + str(len(cd.deck)))
print("3 random cards:")
cd.print_card_list(lst=cd.pick_rand(3))
print("length of deck: " + str(len(cd.deck)))

print("\n\nlength of deck: " + str(len(cd.deck)))
print("3 random cards:")
cd.print_card_list(lst=cd.pick_rand(3, destructive=False))
print("length of deck: " + str(len(cd.deck)))

