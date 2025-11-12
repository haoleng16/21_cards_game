import random

# 扑克牌花色
NUMBERS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
COLORS = ["♠","♥","♦","♣"]

class Card:
    #key
    def __init__(self, number, color):
        self.number = number
        self.color = color
    #key
    def __str__(self):
        return f"{self.color}{self.number}"
    #key
    # def __add__(self, other):
    #     sums = 0
    #     # key
    #     for card in [self, other]:
    #         if card.number == "A":
    #             sums += 1
    #         elif card.number in ["J","Q","K"]:
    #             sums += 10
    #         else:
    #             sums += int(card.number)
    #     return sums
    @staticmethod
    def get_value(cards: list) -> int:
        # key
        cards = [ card.number for card in cards ]
        # A 在总数大于等于 20 时， 算 1 
        value = 0
        for card in cards:
            if card == "A":
                value += 11
            elif card in ["J","Q","K"]:
                value += 10
            else:
                value += int(card)
        # key
        while value > 21 and "A" in cards:
            value -= 10
        return value


class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        #key
        self.cards = [Card(number, color) for number in NUMBERS for color in COLORS]
        #key
        random.shuffle(self.cards)

    def deal_card(self):
        #key
        if len(self.cards) == 0:
            self.reset()
        return self.cards.pop()

    def last_cards(self):
        #key
        return len(self.cards)
