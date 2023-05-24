import math

# 定义一个函数计算组合数
def combination(n, k):
  # 如果n或k不是整数或者n小于k或者n或k小于0，则返回0
  if not isinstance(n, int) or not isinstance(k, int) or n < k or n < 0 or k < 0:
    return 0
  # 否则返回n!/(k!*(n-k)!)，即C(n,k)
  else:
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

# 定义一个函数，计算一张牌的点力
def card_point(card):
  # 如果是A，返回4点
  if card == 'A':
    return 4
  # 如果是K，返回3点
  elif card == 'K':
    return 3
  # 如果是Q，返回2点
  elif card == 'Q':
    return 2
  # 如果是J，返回1点
  elif card == 'J':
    return 1
  # 其他牌，返回0点
  else:
    return 0

# 定义一个函数，计算一手牌的点力
def hand_point(hand):
  # 初始化点力为0
  point = 0
  # 遍历每张牌，累加其点力
  for card in hand:
    point += card_point(card)
  # 返回点力
  return point

# 定义一个函数，计算一手牌是否满足牌型分布和点力范围的要求
def match_hand(hand, shape, point_range):
#   # 初始化四个花色的张数为0
#   spade = 0
#   heart = 0
#   diamond = 0
#   club = 0
#   # 遍历每张牌，根据花色增加相应的张数
#   for card in hand:
#     if card[1] == 'S':
#       spade += 1
#     elif card[1] == 'H':
#       heart += 1
#     elif card[1] == 'D':
#       diamond += 1
#     elif card[1] == 'C':
#       club += 1
#   # 判断是否满足牌型分布的要求，如果不满足，返回False
#   if spade != shape[0] or heart != shape[1] or diamond != shape[2] or club != shape[3]:
#     return False
  # 判断是否满足点力范围的要求，如果不满足，返回False
  point = hand_point(hand)
  if point < point_range[0] or point > point_range[1]:
    return False
  # 如果都满足，返回True
  return True

# # 定义一个函数，计算所有可能的13张手牌的总数，满足牌型分布和点力范围的要求
# def count_hand(shape, point_range):
#   # 初始化总数为0
#   count = 0
#   # 定义所有可能的牌面值和花色
#   values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
#   suits = ['S','H','D','C']
  
#   # 用itertools模块生成所有可能的13张手牌的组合
#   import itertools
#   from tqdm import tqdm
#   hands = itertools.combinations(itertools.product(values, suits), 13)
#   # 遍历每一种组合，判断是否满足要求，如果满足，增加总数
#   total = len(list(hands))
#   print(total)
# #   for hand in tqdm(hands, total=total):
#   for hand in hands:
#     if match_hand(hand, shape, point_range):
#       count += 1
#   # 返回总数
#   return count

# 定义一个函数，计算所有可能的13张手牌的总数，满足牌型分布和点力范围的要求，并显示进度条
def count_hand(shape, point_range):
  # 初始化总数为0
  count = 0
  # 定义所有可能的牌面值和花色
  values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
  suits = ['S','H','D','C']
  def generate_cards(indexes):
    hand = []
    for i in range(4):
      assert len(indexes[i]) == shape[i]
      for v in indexes[i]:
        hand.append((values[v], suits[i]))
    yield hand

  # 定义一个函数，用于生成所有可能的13张手牌的组合，用一个四维数组表示每个花色的牌面值的索引
  def generate_hands():
    import itertools
    for spades in itertools.combinations(range(13), shape[0]):
        for hearts in itertools.combinations(range(13), shape[1]):
            for diamonds in itertools.combinations(range(13), shape[2]):
                for clubs in itertools.combinations(range(13), shape[3]):
                    yield generate_cards([list(spades), list(hearts), list(diamonds), list(clubs)])
    # # 如果已经生成了13张牌，返回这个组合
    # if sum(indexes) == 13:
    #   hand = []
    #   for i in range(4):
    #     for j in range(indexes[i]):
    #       hand.append((values[j], suits[i]))
    #   yield hand
    # # 否则，对于当前花色，尝试每种可能的牌面值的索引，递归生成剩余的牌
    # else:
    #   suit = sum(indexes) // 13
    #   start = indexes[suit]
    #   end = min(13 - sum(indexes), 13)
    #   for i in range(start, end):
    #     indexes[suit] = i
    #     yield from generate_hands(indexes)
    #     indexes[suit] = start
  
  # 计算所有可能的组合的总数，用于显示进度条
  total = 1
  for i in range(4):
    total *= combination(13, shape[i])
#   for i in range(14):
#     for j in range(14 - i):
#       for k in range(14 - i - j):
#         total += 1
  
  # 导入tqdm模块，用于显示进度条
  from tqdm import tqdm
  # 遍历每一种组合，判断是否满足要求，如果满足，增加总数，并显示进度条
  for hand in tqdm(generate_hands(), total=total):
    if match_hand(hand, shape, point_range):
      count += 1
  # 返回总数
  return count



print(count_hand([5,3,3,2], (12,15)))