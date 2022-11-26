import random


class Card:
    """Glorified tuple. Has functions for checking suit, value conveniently."""

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_s(self):
        return self.suit

    def get_v(self):
        return self.value

    def to_string(self):
        return self.get_s() + str(self.get_v())

    def is_value_card(self):
        return (self.get_s() == "H") or (self.get_s() == "S" and self.get_v() == 12) or (
                self.get_s() == "R" and self.get_v() == 10)


class CardSet:
    """
    A glorified list class used both for the deck of self and the players' hands. Has functions for picking random
    self, and shuffling. Starts empty but can be populated with 52 self using the generate_full_deck method.
    """

    def __init__(self, **kwargs):
        self.set = []
        self.size = len(self.set)
        if kwargs.get("populate", False):
            self.generate_full_deck()

    def clear(self):
        self.set = []
        self.size = len(self.set)

    def generate_full_deck(self):
        """
        Generates full 52-card list on in H => S => R => K order.
        :return:
        """
        for s in ["H", "S", "R", "K"]:
            for v in range(2, 15):
                self.set.append(Card(s, v))
        self.size = len(self.set)

    def print_card_list(self):
        """

        :param lst: Kwarg specifying which array of self to pretty-print. Defaults to the deck stored in the class.
        :return: N/A
        """
        for c in self.set:
            print(c.to_string(), end=" ")
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

    def sort(self, **kwargs):  # Suits aren't sorted alphabetically, but in custom HSRK order.
        self.set = sorted(self.set, key=lambda x: x.get_v() + 13 * {"H": 1, "S": 2, "R": 3, "K": 4}[x.get_s()],
                          reverse=kwargs.get("reverse_sort", False))

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
            self.size = len(self.set)
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
            if c.get_s() == s.upper() and c.get_v() == v:
                return c
        return False

    def get_cards_of_suit(self, s, **reverse_sort):
        reverse_sort = reverse_sort.get("reverse_sort", False)
        rcs = CardSet()
        if type(s) is not list:
            s = [s]
        for suit in s:
            for c in self.set:
                if c.get_s() == suit:
                    rcs.add_cards([c])
        rcs.sort(reverse_sort=reverse_sort)
        return rcs

    def get_highest_of_suit(self, s):
        suit_cards = self.get_cards_of_suit(s)
        if suit_cards.size > 0:
            highest = Card("", 0)
            for card in suit_cards.set:
                if card.get_v() > highest.get_v():
                    highest = card
            return highest
        else:
            return False

    def get_lowest_of_suit(self, s):
        suit_cards = self.get_cards_of_suit(s)
        if suit_cards.size > 0:
            lowest = Card("", 20)
            for card in suit_cards.set:
                if card.get_v() < lowest.get_v():
                    lowest = card
            return lowest
        else:
            return False

    def get_highest_of_suit_under_v(self, s, v):
        suit_cards = self.get_cards_of_suit(s)
        if suit_cards.size > 0:
            highest = Card("", 0)
            changed = False
            for card in suit_cards.set:
                if highest.get_v() < card.get_v() < v:
                    highest = card
                    changed = True
            if changed:
                return highest
        return False

    def get_lowest_of_suit_above_v(self, s, v):
        suit_cards = self.get_cards_of_suit(s)
        if suit_cards.size > 0:
            lowest = Card("", 20)
            changed = False
            for card in suit_cards.set:
                if v < card.get_v() < lowest.get_v():
                    lowest = card
                    changed = True
            if changed:
                return lowest
        return False

    def add_cards(self, arr, **kwargs):
        for card in arr:
            try:
                self.set.append(card)
            except ValueError:
                print(card[0] + str(card[1]) + " is not in the deck!")
        if kwargs.get("resort", False):
            self.sort()
        self.size = len(self.set)

    def remove_cards(self, arr, **kwargs):
        for card in arr:
            self.set.remove(card)
        if kwargs.get("resort", False):
            self.sort()
        self.size = len(self.set)
