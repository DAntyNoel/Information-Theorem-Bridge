# import json
# dicts = {}
# dicts[(0,0)] = 1
# with open('test.json', 'w') as f:
#     json.dump(dicts, f, sort_keys=True, ensure_ascii=False, indent=4)

l = [5,3,2,4]
ptt = ''.join(str(i) for i in sorted(l,reverse=True))
print(ptt)
print(l)


import json
def max_distribution_for_pt():
    dicts = {}
    for pt in generate_pt():
        pttt = sorted(pt, reverse=True)
        ptt = ''.join(str(i) for i in pttt)
        if ptt in dicts.keys():
            continue

        info = {
            'cnt':0,
            'detail':[],
            'distribution':[]
        }
        for distribution in generate_distribute():
            cnt = count_suits(distribution, pt)
            info['detail'].append(cnt)
            info['cnt'] += cnt
            info['distribution'].append(distribution)
        
        assert len(info['detail']) == TTL_DISTRIBUTE
        assert sum(info['detail']) == info['cnt']
        
    
        ttl = info['cnt']
        if ttl == 0:
            dicts[ptt] = []
            continue
        probs = {}
        prob = {}
        pr = 0

        for i in range(TTL_DISTRIBUTE):
            disstr = ''.join(str(ii) for ii in sorted(info['distribution'], reverse=True))
            if disstr in probs.keys():
                probs[disstr] += info['detail']
            else:
                probs[disstr] = info['detail']

        for num, distribution in sorted(probs,reverse=True):
            pr += num / ttl
            assert pr <= 1
            prob.update({distribution: num / ttl})
            if pr > 0.8:
                break
        dicts[ptt] = prob