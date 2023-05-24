import json, math

# 286 
TTL_PT = 286
def generate_pt():
  for a1 in range(0, 11):
    for a2 in range(0, 11 - a1):
      for a3 in range(0, 11 - a1 - a2):
        a4 = 10 - a1 - a2 - a3
        yield [a1, a2, a3, a4]

# 6690585616
TTL_PTS = 6690585616
def generate_pts():
  with open('table_distribution_for_pt.json', 'r') as f:
    dicts:dict = json.load(f)
    f.close()
  for a1 in range(0, 11):
    for a2 in range(0, 11 - a1):
      for a3 in range(0, 11 - a1 - a2):
        a4 = 10 - a1 - a2 - a3
        ptt = ''.join(str(i) for i in sorted([a1, a2, a3, a4], reverse=True))
        if ptt not in dicts.keys():
            continue
        for b1 in range(0, 11):
          for b2 in range(0, 11 - b1):
            for b3 in range(0, 11 - b1 - b2):
              b4 = 10 - b1 - b2 - b3
              ptt = ''.join(str(i) for i in sorted([b1, b2, b3, b4], reverse=True))
              if ptt not in dicts.keys():
                continue
              for c1 in range(0, 11):
                for c2 in range(0, 11 - c1):
                  for c3 in range(0, 11 - c1 - c2):
                    c4 = 10 - c1 - c2 - c3
                    ptt = ''.join(str(i) for i in sorted([c1, c2, c3, c4], reverse=True))
                    if ptt not in dicts.keys():
                        continue
                    for d1 in range(0, 11):
                      for d2 in range(0, 11 - d1):
                        for d3 in range(0, 11 - d1 - d2):
                          d4 = 10 - d1 - d2 - d3
                          ptt = ''.join(str(i) for i in sorted([d1, d2, d3, d4], reverse=True))
                          if ptt not in dicts.keys():
                            continue
                          yield [[a1, a2, a3, a4], [b1, b2, b3, b4], [c1, c2, c3, c4], [d1, d2, d3, d4]]

# 560
TTL_DISTRIBUTE = 560
def generate_distribute():
  for a1 in range(0, 14):
    for a2 in range(0, 14 - a1):
      for a3 in range(0, 14 - a1 - a2):
        a4 = 13 - a1 - a2 - a3
        yield [a1, a2, a3, a4]

# 37478624
TTL_DISTRIBUTES = 37478624
def generate_distributes():
  for a1 in range(0, 14):
    for a2 in range(0, 14 - a1):
      for a3 in range(0, 14 - a1 - a2):
        a4 = 13 - a1 - a2 - a3
        for b1 in range(0, 14 - a1):
          for c1 in range(0, 14 - a1 - b1):
            d1 = 13 - a1 - b1 - c1
            if 0 <= d1 <= 13:
              for b2 in range(0, 14 - a2):
                for c2 in range(0, 14 - a2 - b2):
                  d2 = 13 - a2 - b2 - c2
                  if 0 <= d2 <= 13:
                    for b3 in range(0, 14 - a3):
                      for c3 in range(0, 14 - a3 - b3):
                        d3 = 13 - a3 - b3 - c3
                        if 0 <= d3 <= 13:
                          b4 = 13 - b1 - b2 - b3
                          if 0 <= b4 <= 13:
                            c4 = 13 - c1 - c2 - c3
                            if 0 <= c4 <= 13:
                              d4 = 13 - d1 - d2 - d3
                              if 0 <= d4 <= 13:
                                yield [[a1, a2, a3, a4], [b1, b2, b3, b4], [c1, c2, c3, c4], [d1, d2, d3, d4]]

def distribute(scores):
  def check_assign(assignment, scores):
    for i in range(4):
        total = sum(assignment[i])
        if total != scores[i]:
            return False
    return True

  def assign(scores, index, assignment):
    if index == 5:
        if check_assign(assignment, scores):
            yield assignment[:] # yield当前方案的拷贝
    else:
        for i in range(4):
            assignment[i].append(index)
            yield from assign(scores, index + 1, assignment)
            assignment[i].pop()

  assignment = [[] for _ in range(4)]
  yield from assign(scores, 1, assignment)

def count_suits(distribution, pt):
    cnt = 0
    for assignment in distribute(pt):
        x = [0,0,0,0]
        for i in range(4):
            x[i] = distribution[i] - len(assignment[i])
        if x[0] > -1 and x[1] > -1 and x[2] > -1 and x[3] > -1:
            ttl = math.factorial(9)
            for i in range(4):
                ttl //= math.factorial(x[i])
            cnt += ttl
    return cnt   

def max_distribution_for_pt():
    dicts = {}
    for pt in generate_pt():
        ptt = ''.join(str(i) for i in sorted(pt, reverse=True))
        if ptt in dicts.keys():
            continue

        info = {
            'cnt':0,
            'detail':[],
        }
        for distribution in generate_distribute():
            cnt = count_suits(distribution, pt)
            info['detail'].append(cnt)
            info['cnt'] += cnt
        
        assert len(info['detail']) == TTL_DISTRIBUTE
        assert sum(info['detail']) == info['cnt']

        ttl = info['cnt']
        if ttl == 0:
            dicts[ptt] = []
            continue
        probs = []
        prob = {}
        pr = 0
        ii = 0
        for distribution in generate_distribute():
            probs.append((info['detail'][ii], distribution))
            ii += 1

        probss = []
        for ii in range(len(probs)):
            found = False
            disstr = ''.join(str(y) for y in sorted(probs[ii][1], reverse=True))
            for iii in range(len(probss)):
                if disstr == probss[iii][1]:
                    probss[iii][0] += probs[ii][0]
                    found = True
                    break
            if not found:
                probss.append([probs[ii][0], disstr])
        
        probss.sort(key=lambda x: x[0], reverse=True)

        for num, distribution in probss:
            pr += num / ttl
            assert pr <= 1
            prob.update({distribution: num / ttl})
            if pr > 0.8:
                break
        dicts[ptt] = prob
    
    with open('distribution_for_pt.json', 'w') as f:
        json.dump(dicts, f, sort_keys=True, ensure_ascii=False, indent=4)
        f.close()
        
def main():
    with open('table_distribution_for_pt.json', 'r') as f:
        dicts:dict = json.load(f)
        f.close()
    cnt = 0
    for pts in generate_pts():
        for distribution0 in generate_distribute():
            ptt0 = ''.join(str(i) for i in sorted(pts[0], reverse=True))
            disstr0 = ''.join(str(y) for y in sorted(distribution0, reverse=True))
            if ptt0 not in dicts.keys():
                break
            if disstr0 not in dicts[ptt0].keys():
                continue
            for distribution1 in generate_distribute():
                ptt1 = ''.join(str(i) for i in sorted(pts[1], reverse=True))
                disstr1 = ''.join(str(y) for y in sorted(distribution1, reverse=True))
                if ptt1 not in dicts.keys():
                    break
                if disstr1 not in dicts[ptt1].keys():
                    continue
                for distribution2 in generate_distribute():
                    ptt2 = ''.join(str(i) for i in sorted(pts[2], reverse=True))
                    disstr2 = ''.join(str(y) for y in sorted(distribution2, reverse=True))
                    if ptt2 not in dicts.keys():
                        break
                    if disstr2 not in dicts[ptt2].keys():
                        continue
                    for distribution3 in generate_distribute():
                        ptt3 = ''.join(str(i) for i in sorted(pts[3], reverse=True))
                        disstr3 = ''.join(str(y) for y in sorted(distribution3, reverse=True))
                        if ptt3 not in dicts.keys():
                            break
                        if disstr3 not in dicts[ptt3].keys():
                            continue
                        cnt += dicts[ptt0][disstr0] * dicts[ptt1][disstr1] * dicts[ptt2][disstr2] + dicts[ptt3][disstr3]
                        print(cnt)

    return cnt


def table():
    with open('distribution_for_pt.json', 'r') as f:
        dicts:dict = json.load(f)
        f.close()
    table_dicts = {}
    for pt in generate_pt():
        ptt = ''.join(str(i) for i in sorted(pt, reverse=True))
        if ptt not in dicts.keys():
            continue
        table_dicts[ptt] = {}
        for distribution in generate_distribute():
            disstr = ''.join(str(y) for y in sorted(distribution, reverse=True))
            if disstr not in dicts[ptt].keys():
                continue
            table_dicts[ptt][disstr] = count_suits(distribution, pt)
    
    with open('table_distribution_for_pt.json', 'w') as f:
        json.dump(table_dicts, f, sort_keys=True, ensure_ascii=False, indent=4)
        f.close()
        
# main()


# # 定义一个函数，用于计算以下问题：袋子里有13个不同球，其中有4个球分别标有4/3/2/1分，其余球0分。现将其按照数量分给4个人每个人索要的球都数量和分数给定，求可能的分法总数。输入两个数组，第一个数组代表每个人要的球的数量，第二个数组代表要的分数
# def count_ways(ball_counts, ball_scores):
#   # 初始化总数为0
#   total = 0
#   # 定义一个函数，用于生成所有可能的13张手牌的组合，用一个四维数组表示每个花色的牌面值的索引
#   def generate_hands(indexes):
#     # 如果已经生成了13张牌，返回这个组合
#     if sum(indexes) == 13:
#       hand = []
#       for i in range(4):
#         for j in range(indexes[i]):
#           hand.append((i + 1, j + 1))
#       yield hand
#     # 否则，对于当前花色，尝试每种可能的牌面值的索引，递归生成剩余的牌
#     else:
#       suit = sum(indexes) // 13
#       start = indexes[suit]
#       end = min(13 - sum(indexes), 13)
#       for i in range(start, end):
#         indexes[suit] = i
#         yield from generate_hands(indexes)
#         indexes[suit] = start
  
#   # 定义一个函数，用于判断一种分配是否满足要求
#   def match_hand(hand, ball_counts, ball_scores):
#     # 将手牌按照花色分成四份
#     parts = []
#     for i in range(4):
#       part = [card for card in hand if card[0] == i + 1]
#       parts.append(part)
#     # 遍历每一份，判断是否满足数量和分数的要求
#     for i in range(4):
#       part = parts[i]
#       # 如果数量不符合，返回False
#       if len(part) != ball_counts[i]:
#         return False
#       # 计算分数
#       score = 0
#       for card in part:
#         score += card[1]
#       # 如果分数不符合，返回False
#       if score != ball_scores[i]:
#         return False
#     # 如果都符合，返回True
#     return True
  
#   # 遍历所有可能的组合，判断是否满足要求，如果满足，增加总数
#   for hand in generate_hands([0,0,0,0]):
#     if match_hand(hand, ball_counts, ball_scores):
#       total += 1
  
#   # 返回总数
#   return total


# cnt = 0
# for i in generate_distributes():
#     cnt += 1
# print(cnt)
# cnt = 0
# for i in generate_pts():
#     cnt += 1
# print(cnt)