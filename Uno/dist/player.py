class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.gain_card = 0
        self.choose_cards = []
        self.can_buy = True
        self.section = 0
    
    def remove_card(self, index):
        self.cards.pop(index)

    def remove_choose_card(self, index):
        self.choose_cards.pop(index)
    
    def reset_chcards(self):
        self.choose_cards = []

    def get_qnt_chcards(self):
        return len(self.choose_cards)
    
    def get_last_chcard_index(self):
        return self.choose_cards[self.get_qnt_chcards()-1]

    def get_last_chcard(self):
        return self.cards[self.get_last_chcard_index()]
    
    def get_chcard_index(self, index):
        return self.choose_cards[index]

    def get_chcard(self, index):
        return self.cards[self.get_chcard_index(index)]

    def get_card(self, index):
        return self.cards[index]

    def get_qnt_cards(self):
        return len(self.cards)

    def buy_card(self, card):
        self.cards.append(card)