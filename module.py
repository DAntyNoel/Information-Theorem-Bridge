class Card():
    """A playing card."""
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    SUITS = ['♠️', '♥️', '♦️', '♣️']

    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.is_face_up = face_up  # 是否显示牌的正面

    def __str__(self):  # 重写print方法，打印一张牌的信息
        if self.is_face_up:
            rep = self.suit + self.rank
        else:
            rep = 'XX'
        return rep

    def pic_order(self):  # 牌的顺序号
        if self.rank == 'A':
            FaceNum = 1
        elif self.rank == 'J':
            FaceNum = 11
        elif self.rank == 'Q':
            FaceNum = 12
        elif self.rank == 'K':
            FaceNum = 13
        elif self.rank == 'T':
            FaceNum = 10
        else:
            FaceNum = int(self.rank)
        if self.suit == '♣️':
            Suit = 1
        elif self.suit == '♦️':
            Suit = 2
        elif self.suit == '♥️':
            Suit = 3
        else:
            Suit = 4
        return (Suit-1) * 13 + FaceNum

    def flip(self):  # 翻牌方法
        self.is_face_up = not self.is_face_up

    def order(rank):
        if rank == 'A':
            FaceNum = 14
        elif rank == 'J':
            FaceNum = 11
        elif rank == 'Q':
            FaceNum = 12
        elif rank == 'K':
            FaceNum = 13
        elif rank == 'T':
            FaceNum = 10
        else:
            FaceNum = int(rank)
        return FaceNum


class Hand():
    """A hand of playing cards"""
    def __init__(self):
        self.cards = []  # cards列表变量存储牌手中的牌

    def __str__(self):
        try:
            self.sort
        except:
            self.check()
        rep = ''
        for t in range(4):
            rep += '\n' + Card.SUITS[t]
            for i in self.sort[t]:
                rep += ' '
                rep += i
        # rep = Card.SUITS[0]
        # for i in self.S:
        #     rep += ' '
        #     rep += i
        # rep += '\n' + Card.SUITS[1]
        # for i in self.H:
        #     rep += ' '
        #     rep += i
        # rep += '\n' + Card.SUITS[2]
        # for i in self.D:
        #     rep += ' '
        #     rep += i
        # rep += '\n' + Card.SUITS[3]
        # for i in self.C:
        #     rep += ' '
        #     rep += i
        return rep[1:]
    
    def display(self) -> list:
        rep = ["","","",""]
        try:
            self.done
        except:
            self.check()
        for t in range(4):
            rep[t] = Card.SUITS[t]
            for i in self.sort[t]:
                rep[t] += ' '
                rep[t] += i
            if len(self.sort[t]) < 1:
                rep[t] += ' -'
        # rep[0] = Card.SUITS[0]
        # for i in self.S:
        #     rep[0] += ' '
        #     rep[0] += i
        # if len(self.S) < 1:
        #     rep[0] += ' -'
        # rep[1] = Card.SUITS[1]
        # for i in self.H:
        #     rep[1] += ' '
        #     rep[1] += i
        # if len(self.H) < 1:
        #     rep[1] += ' -'
        # rep[2] = Card.SUITS[2]
        # for i in self.D:
        #     rep[2] += ' '
        #     rep[2] += i
        # if len(self.D) < 1:
        #     rep[2] += ' -'
        # rep[3] = Card.SUITS[3]
        # for i in self.C:
        #     rep[3] += ' '
        #     rep[3] += i
        # if len(self.C) < 1:
        #     rep[3] += ' -'
        return rep

    def clear(self):  # 清空手里的牌
        self.cards = []
        self.sort = None

    def add(self, card):  # 增加牌
        self.cards.append(card)

    def give(self, card, other_hand):  # 把一张牌给其他牌手
        self.cards.remove(card)
        other_hand.add(card)
    
    def check(self):
        if len(self.cards) != 13:
            print(f'错误的手牌张数：{len(self.cards)}')
            return
        self.sort = [[], [], [], []]
        self.pt = 0
        for card in self.cards:
            if card.rank == 'J':
                self.pt += 1
            elif card.rank == 'Q':
                self.pt += 2
            elif card.rank == 'K':
                self.pt += 3
            elif card.rank == 'A':
                self.pt += 4
            if card.suit == Card.SUITS[0]:
                self.sort[0].append(card.rank)
            elif card.suit == Card.SUITS[1]:
                self.sort[1].append(card.rank)
            elif card.suit == Card.SUITS[2]:
                self.sort[2].append(card.rank)
            elif card.suit == Card.SUITS[3]:
                self.sort[3].append(card.rank)
        for i in range(4):
            self.sort[i].sort(reverse=True, key=Card.order)


class Poke(Hand):
    """A deck of playing cards."""
    def populate(self):  # 生成一副牌
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))

    def shuffle(self):  # 洗牌
        import random
        random.shuffle(self.cards)  # 打乱牌的顺序

    def deal(self, hands, per_hand=13):  # 发牌，发给玩家，每人默认13张牌
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card=self.cards[0]
                    self.cards.remove(top_card)
                    hand.add(top_card)
                    # self.give(top_card, hand)  # 上面的两句可以用这一句代替
                else:
                    print('牌已发完！')


def display_game(players):
    N:list = players[0].display()
    E:list = players[1].display()
    S:list = players[2].display()
    W:list = players[3].display()
    max_N = max([len(i) for i in N])
    max_W = max([len(i) for i in W])
    max_S = max([len(i) for i in S])
    max_NS = max(max_N, max_S)
    ret = '\n'
    space = ' '
    ret += space * 3 + str(players[0].pt) + space * (max_W - 3 - len(str(players[0].pt))) + N[0] + '\n'
    ret += str(players[3].pt) + space * (5 - len(str(players[3].pt)) + 1) + str(players[1].pt) + space * (max_W - 7 - len(str(players[1].pt)) + 1) + N[1] + '\n'
    ret += space * 3 + str(players[2].pt) + space * (max_W - 3 - len(str(players[2].pt))) + N[2] + '\n'
    ret += space * max_W + N[3] + '\n'
    for t in range(4):
        ret += W[t] + space * (max_W - len(W[t]) + max_NS + 1) + E[t] + '\n'
    for t in range(4):
        ret += space * max_W + S[t] + '\n'
    return ret

def clip_board(players):
    N:list = players[0].display()
    E:list = players[1].display()
    S:list = players[2].display()
    W:list = players[3].display()
    max_N = max([len(i) for i in N]) - 2
    max_W = max([len(i) for i in W]) - 2
    max_S = max([len(i) for i in S]) - 2
    max_NS = max(max_N, max_S)
    ret = ''
    space = ' '
    # ret += space * 3 + str(players[0].pt) + space * (max_W - 3 - len(str(players[0].pt))) + N[0] + '\n'
    # ret += str(players[3].pt) + space * (5 - len(str(players[3].pt)) + 1) + str(players[1].pt) + space * (max_W - 7 - len(str(players[1].pt)) + 1) + N[1] + '\n'
    # ret += space * 3 + str(players[2].pt) + space * (max_W - 3 - len(str(players[2].pt))) + N[2] + '\n'
    # ret += space * max_W + N[3] + '\n'
    for t in range(4):
        ret += space * max_W + N[t][2:] + '\n'
    for t in range(4):
        ret += W[t][2:] + space * (max_W - len(W[t]) + max_NS + 1) + E[t][2:] + '\n'
    for t in range(4):
        ret += space * max_W + S[t][2:] + '\n'

    import pyperclip
    pyperclip.copy(ret)
    print('已复制到剪贴板')

def PBN_str(players):
    ret = 'N:'
    for i in range(4):
        hand:Hand = players[i]
        for t in range(4):
            for c in hand.sort[t]:
                ret += c
            if t < 3:
                ret += '.'
        if i < 3:
            ret += ' '
    print(ret)
    return ret



if __name__ == "__main__":
    # print('扑克发牌开始：')
    # 4个玩家
    for i in range(3):
        players = [Hand(), Hand(), Hand(), Hand()]
        poke1 = Poke()
        poke1.populate()  # 生成一副牌
        poke1.shuffle()  # 洗牌
        poke1.deal(players, 13)  # 发给每个玩家13张牌
        # 显示4位牌手的牌
        # n = 1
        # for hand in players:
        #     hand.check()
        #     print('牌手', n, ':', hand.pt)
        #     print(hand)
        #     n = n + 1
        # input('\n Press the enter key to exit.')
        print(display_game(players))
        pbn = PBN_str(players)
        # clip_board(players)

        from CalcAllTablesPBN import *
        calcdds(pbn)
    
