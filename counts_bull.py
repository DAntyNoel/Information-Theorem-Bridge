# 导入math模块
import math

# 定义一个函数计算组合数
def combination(n, k):
  # 如果n或k不是整数或者n小于k或者n或k小于0，则返回0
  if not isinstance(n, int) or not isinstance(k, int) or n < k or n < 0 or k < 0:
    return 0
  # 否则返回n!/(k!*(n-k)!)，即C(n,k)
  else:
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

# 定义一个函数计算给定花色长度时可能的花色分布数量
def suit_distribution(length):
  # 如果长度不是整数或者长度小于0或者长度大于13，则返回0
  if not isinstance(length, int) or length < 0 or length > 13:
    return 0
  # 否则返回C(13,length)，即从13张牌中选length张牌的组合数
  else:
    return combination(13, length)

# 定义一个函数计算给定点力范围时可能的点力分布数量
def point_distribution(min_point, max_point):
  # 如果最小点或最大点不是整数或者最小点小于0或者最大点大于40或者最小点大于最大点，则返回0
  if not isinstance(min_point, int) or not isinstance(max_point, int) or min_point < 0 or max_point > 40 or min_point > max_point:
    return 0
  # 否则初始化一个变量count为0，用来记录可能的分布数量
  else:
    count = 0
    # 遍历所有可能的A、K、Q、J、10的数量（分别记为a,k,q,j,t），每张牌对应4个点力
    for a in range(5):
      for k in range(5):
        for q in range(5):
          for j in range(5):
            for t in range(5):
              # 计算当前组合对应的总点力
              point = a * 4 + k * 3 + q * 2 + j + t
              # 如果总点力在给定范围内，则计算当前组合对应的分布数量，并累加到count中
              if min_point <= point <= max_point:
                # 当前组合对应的分布数量等于从13张牌中选a+k+q+j+t张牌，并且从剩下的4-a张A中选a张A，
                # 从剩下的4-k张K中选k张K，以此类推，最后相乘得到结果
                count += combination(13, a + k + q + j + t) * combination(4 - a, a) * combination(4 - k, k) * combination(4 - q, q) * combination(4 - j, j) * combination(4 - t, t)
    # 返回count作为结果
    return count

# 定义一个函数计算给定花色长度和点力范围时可能的手牌分布数量
def hand_distribution(length, min_point, max_point):
  # 如果长度不是整数或者长度小于0或者长度大于13，则返回0
  if not isinstance(length, int) or length < 0 or length > 13:
    return 0
  # 否则初始化一个变量count为0，用来记录可能的分布数量
  else:
    count = 0
    # 遍历所有可能的该花色长度对应的点力（记为point），从最小点到最大点
    for point in range(min_point, max_point + 1):
      # 计算该花色长度和点力对应的花色分布数量和剩余三个花色对应的点力分布数量，并相乘得到当前组合对应的手牌分布数量，并累加到count中
      count += suit_distribution(length) * point_distribution(min_point - point, max_point - point)
    # 返回count作为结果
    return count

# 定义一个常量表示总的手牌分布数量（53兆多）
TOTAL_HANDS = math.factorial(52) // (math.factorial(13) ** 4)

# 定义一个函数计算给定条件下可能满足条件的手牌分布概率（百分比）
def hand_probability(length1, min_point1, max_point1, length2, min_point2, max_point2):
  # 计算庄家和明手各自可能满足条件的手牌分布数量，并相乘得到联手可能满足条件的手牌分布数量（记为possible_hands）
  possible_hands = hand_distribution(length1, min_point1, max_point1)
# 计算防守方可能满足条件的手牌分布数量，并相乘得到联手可能满足条件的手牌分布数量（记为impossible_hands）
  # 防守方的条件是黑桃长度不超过2，点力不超过10
  impossible_hands = hand_distribution(0, 0, 10) * hand_distribution(0, 0, 10) + hand_distribution(1, 0, 10) * hand_distribution(1, 0, 10) + hand_distribution(2, 0, 10) * hand_distribution(2, 0, 10)
  # 计算可能满足条件的手牌分布概率，即possible_hands除以TOTAL_HANDS减去impossible_hands，然后乘以100，并保留两位小数
  probability = round(possible_hands / (TOTAL_HANDS - impossible_hands) * 100, 2)
  # 返回概率作为结果
  return probability

# 定义一个函数打印给定条件下可能满足条件的手牌分布概率（百分比）
def print_probability(length1, min_point1, max_point1, length2, min_point2, max_point2):
  # 调用hand_probability函数计算概率，并赋值给变量p
  p = hand_probability(length1, min_point1, max_point1, length2, min_point2, max_point2)
  # 打印结果，格式为“庄家：黑桃长度为length1，点力范围为min_point1-max_point1；明手：黑桃长度为length2，点力范围为min_point2-max_point2。可能满足条件的手牌分布概率为p%。”
  print(f"庄家：黑桃长度为{length1}，点力范围为{min_point1}-{max_point1}；明手：黑桃长度为{length2}，点力范围为{min_point2}-{max_point2}。可能满足条件的手牌分布概率为{p}%。")

# 调用print_probability函数，输入叫牌过程为1S-2S-4S时定约方的条件，即庄家黑桃长度不低于5，点力范围为12-15；明手黑桃长度不低于4，点力范围为6-10
print_probability(5, 12, 15, 4, 6, 10)


