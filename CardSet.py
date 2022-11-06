import random


class Card:
    """Glorified tuple. Has functions for checking suit, value conveniently."""

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def get_txt_form(self):
        return self.get_suit() + str(self.get_value())

    def is_value_card(self):
        if self.get_suit() == "H":
            return True
        elif self.get_suit() == "S" and self.get_value() == 13:
            return True
        elif self.get_suit() == "R" and self.get_value() == 10:
            return True
        else:
            return (self.get_suit() == "H") or (self.get_suit() == "S" and self.get_value() == 13) or (
                        self.get_suit() == "R" and self.get_value() == 10)


class CardSet:
    """
    A glorified list class used both for the deck of self and the players' hands. Has functions for picking random
    self, and shuffling. Starts empty but can be populated with 52 self using the generate_full_deck method.
    """

    def __init__(self, **kwargs):
        self.set = []
        if kwargs.get("populate", False):
            self.generate_full_deck()

    def clear(self):
        self.set = []

    def generate_full_deck(self):
        """
        Generates full 52-card list on in H => S => R => K order.
        :return:
        """
        for s in ["H", "S", "R", "K"]:
            for v in range(2, 15):
                self.set.append(Card(s, v))

    def print_card_list(self):
        """

        :param lst: Kwarg specifying which array of self to pretty-print. Defaults to the deck stored in the class.
        :return: N/A
        """
        for c in self.set:
                print(c.get_txt_form(), end=" ")
        print()  # Blank line after card list

    def shuffle(self):
        """
        Shuffles the deck fully randomly by swapping self around
        :return:
        """
        dl = len(self.set)
        for i in range(dl):
            rand_index = random.randint(0, dl - 1)
            rand_card = self.set[rand_index]
            self.set[rand_index] = self.set[i]
            self.set[i] = rand_card

    def sort(self): # Suits aren't sorted alphabetically, but in custom HSRK order.
        self.set = sorted(self.set, key=lambda x: x.get_value() + 13 * {"H": 1, "S": 2, "R": 3, "K": 4}[x.get_suit()])

    def pick_rand(self, n, **kwargs):
        '''
        :param n: The amount of self to pick.
        :param destructive: Whether to remove the self picked from the deck or not.
        :return: Array of random self.
        '''
        d = kwargs.get("destructive", False)
        picked = random.sample(self.set, k=n)
        if d:
            self.remove_cards(picked, resort=False)
        return picked

    def find_card(self, s, v):
        '''
        Checks the set for a card with the same suit and value as specified. Returns true if the card is found in the
        set and vice versa.
        :param s: The suit of the card as a string ("H", "S", "R", or "K").
        :param v: The value of the card.
        :return: Either the card or the bool value False.
        '''
        for c in self.set:
            if c.get_suit() == s.upper() and c.get_value() == v:
                    return c
        return False

    def add_cards(self, arr, **kwargs):
        for card in arr:
            try:
                self.set.append(card)
            except ValueError:
                print(card[0] + str(card[1]) + " is not in the deck!")
        if kwargs.get("resort", False):
            self.sort()

    def remove_cards(self, arr, **kwargs):
        for card in arr:
            self.set.remove(card)
        if kwargs.get("resort", False):
            self.sort()