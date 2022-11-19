from AgentBaseClass import AgentBaseClass
from random import sample

class RandomAgent(AgentBaseClass):
    def __init__(self, name):
        super(RandomAgent, self).__init__(name)     # Calls AgentBaseClass __init__, making this function supplementary,
        # for stuff such as setting a memory variable.

    def pick_card(self, trick):
        # print(sample(self.get_legal_cards(trick), 1)[0])
        return sample(self.get_legal_cards(trick), 1)[0]

class FirstIntelliAgent(AgentBaseClass):
    def __init__(self, name):
        super(RandomAgent, self).__init__(name)     # Calls AgentBaseClass __init__, making this function supplementary,
        # for stuff such as setting a memory variable.

    def pick_card(self, trick):
        # print(sample(self.get_legal_cards(trick), 1)[0])
        return sample(self.get_legal_cards(trick), 1)[0]