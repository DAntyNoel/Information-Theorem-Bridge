import random

play = [[[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]]]
spades = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
hearts = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
diamonds = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
clubs = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']



def reset():
    global play 
    global spades
    global hearts
    global diamonds
    global clubs
    suits = [spades, hearts, diamonds, clubs]
    play = [[[],[],[],[]], [[],[],[],[]], [[],[],[],[]], [[],[],[],[]]]
    spades = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    hearts = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    diamonds = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    clubs = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']

def check():
    global play 
    for i in range(4):
        leng = 0
        for suit in play[i]:
            suit.sort(key=order, reverse=True)
            leng += len(suit)
        if leng != 13:
            print(f'Error check: length {leng}')
            return False
    
    for suit in range(4):
        all = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
        try:
            for i in range(4):
                for card in play[i][suit]:
                    all.remove(card)
            if len(all) > 0:
                print('Error check: suit')
                return False
        except:
            print('Error check: suit')
            return False
    
    return True


def draw_suit_cards(hand, suit, num) -> int:
    '''Draw num cards from suit to hand, returns the hcp, -1 if failed'''
    global spades
    global hearts
    global diamonds
    global clubs
    suits = [spades, hearts, diamonds, clubs]
    pt = 0
    if num < 1:
        return -1
    if len(suits[suit]) < num:
        return -1
    for i in range(num):
        card = random.choice(suits[suit])
        suits[suit].remove(card)
        if card == 'A':
            pt += 4
        elif card == 'K':
            pt += 3
        elif card == 'Q':
            pt += 2
        elif card == 'J':
            pt += 1
        hand[suit].append(card)
    return pt

def count_cards(hand):
    num = 0
    for suit in hand:
        num += len(suit)
    return num
def count_pt(hand):
    pt = 0
    for suit in hand:
        for card in suit:
            if card == 'A':
                pt += 4
            elif card == 'K':
                pt += 3
            elif card == 'Q':
                pt += 2
            elif card == 'J':
                pt += 1
    return pt

def supply_cards(hand, minpt = 0, maxpt = 40) -> bool:
    global spades
    global hearts
    global diamonds
    global clubs
    suits = [spades, hearts, diamonds, clubs]
    cnt = count_cards(hand)
    if cnt == 13:
        return True
    if cnt > 13:
        print("Error supply: count")
        return False
    pt_now = count_pt(hand)
    if pt_now > maxpt:
        print("Error supply: pt")
        return False
    remain_cards = count_cards(suits)
    remain_pt = count_pt(suits)
    if cnt + remain_cards == 13:
        if pt_now + remain_pt < minpt or pt_now + remain_pt > maxpt:
            return False
        for i in range(4):
            for y in suits[i]:
                hand[i].append(y)
            suits[i] = []
        return True
    if cnt + remain_cards < 13:
        print("Error supply: less cards")
        return False
    
    wanted_distribute = [0,0,0,0]
    for _ in range(13 - cnt):
        while True:
            suit = random.choice(range(4))
            if len(suits[suit]) > wanted_distribute[suit]:
                wanted_distribute[suit] += 1
                break
        
    
    for _ in range(1000):
        wanted = [[],[],[],[]]
        for suit in range(4):
            wanted[suit] = random.sample(suits[suit], wanted_distribute[suit])
        pt_want = count_pt(wanted)
        if pt_want + pt_now < minpt or pt_want + pt_now > maxpt:
            wanted = [[],[],[],[]]
        else:
            for suit in range(4):
                for card in wanted[suit]:
                    suits[suit].remove(card)
                    hand[suit].append(card)
            return True
    
    print('Error supply: iterations exceeded')
    return False

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

def exchange_suit(a:int,b:int):
    if a == b:
        return True
    global play
    for i in range(4):
        t = play[i][a]
        play[i][a] = play[i][b]
        play[i][b] = t

def make_PBN():
    global play
    pbn = 'N:'
    for i in range(4):
        for suit in range(4):
            for card in play[i][suit]:
                pbn += card
            if suit < 3:
                pbn += '.'
        if i < 3:
            pbn += ' '
    # print(pbn)
    store(pbn)

pbn_storage = []
def store(pbn):
    global pbn_storage
    pbn_storage.append(pbn)
    if len(pbn_storage) % 100 == 99:
        pbn_storage = list(set(pbn_storage))
    if len(pbn_storage) % 100 == 0:
        print(f'PBN collect: {len(pbn_storage)}')

def main_shuffle_unbalanced():
    global play
    reset()
    pt_spades = draw_suit_cards(play[0], 0, 5)
    if pt_spades < 2:
        draw_suit_cards(play[0], 0, 1)
    
    draw_suit_cards(play[2], 0, 3)
    assert supply_cards(play[0], 11, 21)
    if len(play[0][0]) < len(play[0][1]):
        print('W: Hearts longer than Spades')
        return False
    assert supply_cards(play[2], 7)
    if random.choice([0,1]):
        assert supply_cards(play[1])
        assert supply_cards(play[3])
    else:
        assert supply_cards(play[3])
        assert supply_cards(play[1])
    assert check()
    make_PBN()
    return True

def main_shuffle_balanced():
    global play
    
    reset()
    assert supply_cards(play[0])
    assert supply_cards(play[1])
    assert supply_cards(play[2])
    assert supply_cards(play[3])
    pts = [count_pt(hand) for hand in play]
    # print(1, play, pts)
    if max(pts) < 12:
        return False
    for i in range(4):
        if pts[i] >= 11 and pts[i] < 22 and i == 0:
            break
        if pts[i] >= 11 and pts[i] < 22:
            # exchange_hand(play[0], play[i])
            kk = play[0] 
            play[0] = play[i]
            play[i] = kk
            kk = pts[0]
            pts[0] = pts[i]
            pts[i] = kk 
            break
        if i == 3:
            return False
    # print(2, play, pts)
    max_suit = 0
    max_len = 0
    for i in range(4):
        if len(play[0][i]) > max_len:
            max_suit = i
            max_len = len(play[0][i])
    if max_len < 5:
        return False

    exchange_suit(0, max_suit)
    assert check()

    # print(3, play, pts)
    for i in range(1, 4):
        if pts[i] > 5 and len(play[i][0]) >= 3:
            # exchange_hand(play[2], play[i])
            kk = play[2]
            play[2] = play[i]
            play[i] = kk
            kk = pts[2]
            pts[2] = pts[i]
            pts[i] = kk
            assert check()
            # print(4, play, pts)
            make_PBN()
            # print(pts)
            return True
    
    return False


    
def write_pbn():
    global pbn_storage
    with open('pbn.txt', 'w') as f:
        for pbn in pbn_storage:
            f.write(pbn)
            f.write('\n')
        f.close()
# 13黑桃 13其他 12黑桃 12其他 10黑桃 其他局 9黑桃 8黑桃 其他
chinesse = ['黑桃大满贯\t','其他大满贯\t','黑桃小满贯\t','其他小满贯\t','黑桃能成局\t','其他能成局\t','3 黑桃     ','2 黑桃     ','  其他     ']
# chinesse = ['7 黑桃','7 其他','6 黑桃','6 其他','4+黑桃','其他局']
# [1195, 185, 2778, 480, 7923, 870, 2549, 1678, 972]
COUNT = [0,0,0,0,0,0,0,0,0] 
def solve_result(result):
    global COUNT
    for suit in range(5):
        if result[suit][0] == 13 or result[suit][2] == 13:
            if suit == 0:
                if result[suit][0] == 13:
                    COUNT[0] += 1
                    return 0
                else:
                    continue
            else:
                COUNT[1] += 1
                return 1
    for suit in range(5):
        if result[suit][0] == 12 or result[suit][2] == 12:
            if suit == 0:
                if result[suit][0] == 12:
                    COUNT[2] += 1
                    return 2
                else:
                    continue
            else:
                COUNT[3] += 1
                return 3
    
    if result[0][0] >= 10:
        COUNT[4] += 1
        return 4
    
    if result[1][0] >= 10 or result[2][0] >= 11 or result[3][0] >= 11 or result[4][0] >= 9:
        COUNT[5] += 1
        return 5
    if result[1][2] >= 10 or result[2][2] >= 11 or result[3][2] >= 11 or result[4][2] >= 9:
        COUNT[5] += 1
        return 5

    if result[0][0] == 9:
        COUNT[6] += 1
        return 6
    if result[0][0] == 8:
        COUNT[7] += 1
        return 7
    
    COUNT[8] += 1
    return 8

from CalcAllTablesPBN import *
def solve_pbn():
    with open('../pbn_18600.txt', 'r') as f:
        with open('../pbn_18600_result.txt', 'w') as g:
            pbn = f.readline()
            while pbn:
                result = calcdds(pbn)
                g.write(chinesse[solve_result(result)])
                g.write(' | ')
                g.write(pbn)
                pbn = f.readline()
    print(COUNT)

def main():
    for _ in range(30):
        # main_shuffle_unbalanced()
        main_shuffle_balanced()
    write_pbn()

if __name__ == '__main__':
    # main()
    solve_pbn()
    

