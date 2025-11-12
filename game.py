"""
游戏规则:
1.目标是让手牌点数尽可能接近21点但不超过(超过会判负)
2.A可以算作1，J/Q/K算作10点[ok]
3.两张牌总和为21点称为'黑杰克'，赔率1.5倍庄家小于17点必须要牌，大于等于17点停牌
4.点数相同为平局，退还赌注。
"""
import sys
from cards import Deck
from cards import Card

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.cards = []
        self.bet_amount = None

    def add_card(self, card):
        self.cards.append(card)

    # 下注
    def bet(self, amount):
        if amount > self.money:
            print(f"{self.name} 没有足够的资金")
            return False
        self.money -= amount
        self.bet_amount = amount
        return True
    
    # 赢钱
    def win(self, amount):
        self.money += amount
        print(f"{self.name} 赢了{amount - self.bet_amount}元，当前余额{self.money}元")

    # 输钱
    def lose(self, amount):
        # key
        self.money = max(self.money - amount ,0 ) 
        if self.money == 0:
            print(f"{self.name} 没有足够的资金 游戏结束")
            # key
            sys.exit()
        amount += self.bet_amount
        print(f"{self.name} 输了{amount}元，当前余额{self.money}元")

    def show_hand_cards(self):
        # key
        return [ str(card) for card in self.cards ]


class Game:
    def __init__(self, player: Player):
        self.player = player
        self.dealer = Player("庄家", 100000000000000)
        self.deck = Deck()

    # 下注
    def bet(self):
        while True:
            amount = float(input("请输入你的下注金额: "))
            if amount <= 0:
                print("请输入大于0的金额")
                continue
            self.player.bet(amount)
            return amount
    
    # 发牌
    def deal(self):
        self.player.add_card(self.deck.deal_card())
        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

    # 用户选择要牌
    def player_hit(self):
        print(f"玩家的牌是{self.player.show_hand_cards()}")
        while True:
            choice = input("是否要牌(y/n): ").lower()
            if choice == "y":
                self.player.add_card(self.deck.deal_card())
                player_value = Card.get_value(self.player.cards)
                print(f"玩家的牌是{self.player.show_hand_cards()}")
                if player_value > 21:
                    return
                else:
                    continue
            elif choice == "n":
                return
            else:   
                print("请输入y或n")
                continue

    # 庄家自动要牌
    def dealer_hit(self):
        dealer_value = Card.get_value(self.dealer.cards)
        while True:
            if dealer_value < 17:
                self.dealer.add_card(self.deck.deal_card())
                dealer_value = Card.get_value(self.dealer.cards)
            elif dealer_value >= 17:
                break


    def compare(self, amount):
        """
        停牌-比较大小
        """
        print(f"玩家的牌是{self.player.show_hand_cards()}")
        print(f"庄家的牌是{self.dealer.show_hand_cards()}")
        player_value = Card.get_value(self.player.cards)
        dealer_value = Card.get_value(self.dealer.cards)

        if player_value > 21:
            self.player.lose(0)
        elif dealer_value > 21:
            self.player.win(amount * 2)

        # 当玩家和庄家都是21点时，比较牌的数量，玩家数量少赢，否则输
        elif (player_value == 21) and (dealer_value == 21):
            # key
            if len(self.player.cards) >= len(self.dealer.cards) :
                self.player.lose(amount * 0.5)
            elif len(self.player.cards) < len(self.dealer.cards):
                self.player.win(amount * 2.5)
        # 当玩家是21点时，赢1.5倍
        elif player_value == 21 :
            self.player.win(amount * 2.5)
        # 当庄家是21点时，输1.5倍
        elif dealer_value == 21 :
            self.player.lose(amount * 0.5)

        # 正常无倍数输赢
        elif player_value > (dealer_value + 0.5):
            self.player.win(amount * 2)
        elif player_value < (dealer_value - 0.5):
            self.player.lose(0)
        else:
            print("居然出现了我没想到的情况？")


    def reset(self):
        self.player.cards = []
        self.dealer.cards = []

    def start(self):
        while True:
            self.reset()
            amount = self.bet()
            self.deal()
            self.dealer_hit()
            self.player_hit()
            self.compare(amount)
            if self.player.money == 0:
                print("你破产了，游戏结束")
                break
            elif self.dealer.money == 0:
                print("庄家破产了，你赢了")
                break
            else:
                continue


def main():
    ##key
    print(f"""
{"="*20}
游戏规则:
1.目标是让手牌点数尽可能接近21点但不超过
2.A可以算作1或11点，J/Q/K算作10点
3.两张牌总和为21点称为'黑杰克'，赔率1.5倍庄家小于17点必须要牌，大于等于17点停牌
4.点数相同为平局，退还赌注
{"="*20}
""")
    #key
    user_name= input("请输入你的名字: ").replace(" ","") or "玩家"
    print(f"欢迎 \"{user_name}\" 来到21点游戏!")

    while True:
        try:
            #key
            money = float(input("请输入你的初始资金: "))
        except Exception as e:
            print("请输入有效的金额")
            continue

        if money <= 0:
            print("请输入大于0的金额")
            continue
        break
    print(f"你有{money}元")
    game = Game(Player(user_name, money))
    game.start()
    print(f"庄家: {game.dealer.show_hand_cards()}")
    print(f"玩家: {game.player.show_hand_cards()}")



if __name__ == "__main__":
    main()
