NOTRUMP = 'NT'
SPADE = '♠️'
HEART = '♥️'
DIAMOND = '♦️'
CLUB = '♣️'

class Natural:
    pass

def is_balance(distribute:list) -> list:
    redis = sorted(distribute, reverse=True)
    return redis[0] + redis[1] <= 8 and redis[3] >= 2

def reset_pt(pts:list, distribute:list, suit:int) -> int:
    '''以 suit 为将牌计算调整点'''
    if suit == 4 or suit == 5:
        return sum(pts)
    rept = 0
    for t in range(4):
        rept += pts[t]
        if t == suit:
            continue
        if distribute[t] == 2:
            if pts[t] <= 2:
                rept += 1
        if distribute[t] == 1:
            rept += 3
            if pts[4] > 0:
                rept -= 1
        if distribute[t] == 0:
            rept += 5
    
    if distribute[suit] >= 4 and min(distribute) < 3:
        rept += 2 * distribute[suit] - 7
    return rept
            

        

def r0(pts:list, distribute:list):
    '''开叫'''
    pt = sum(pts)

    if pt < 5:
        return 0 # Pass

    if pt >= 15 and pt <= 17 and is_balance(distribute):
        return 15 # 1NT
    
    if pt >= 20 and pt <= 21 and is_balance(distribute):
        return 25 # 2NT
    
    if pt > 21:
        return 21 # 2C

    if pt >= 11 and pt <= 21 and distribute[0] < 5 and distribute[1] < 5 and (distribute[3] > distribute[2] or (distribute[3] == distribute[2] and distribute[3] < 4)):
        return 11 # 1C

    if pt >= 11 and pt <=21 and distribute[0] < 5 and distribute[1] < 5 and (distribute[2] > distribute[3] or (distribute[3] == distribute[2] and distribute[3] >= 4)):
        return 12 # 1D
    
    if pt >= 11 and pt <= 21 and distribute[0] <= distribute[1] and distribute[1] >= 5:
        if distribute[0] == distribute[1]:
            if pt > 15:
                return 13 # 1H 逆叫
            else:
                return 14 # 1S
        else:
            return 13 # 1H
    
    if pt >= 11 and pt <= 21 and distribute[0] >= 5 and distribute[0] > distribute[1]:
        return 14 # 1S
    
    if pt >= 6 and pt <= 10:
        # 阻击叫
        if max(distribute) < 6:
            return 0 # Pass
        if max(distribute) == distribute[0] and distribute[1] < 4:
            return min(distribute[0] - 4, 4) * 10 + 4 # 2S 3S 4S
        if max(distribute) == distribute[1] and distribute[0] < 4:
            return min(distribute[0] - 4, 4) * 10 + 3 # 2H 3H 4H
        if max(distribute) == distribute[2] and distribute[0] < 4 and distribute[1] < 4:
            return min(distribute[0] - 4, 5) * 10 + 2 # 2D 3D 4D 5D
        if max(distribute) == distribute[3] and distribute[0] < 4 and distribute[1] < 4:
            if distribute[3] == 6 and pt > 7:
                return 31 # 3C
            return min(distribute[3] - 4, 5) * 10 + 1 # 3C 4C 5C

    print("bid:0 unused")
    # 无赌博 3NT 

    return 0

def r11(pts:list, distribute:list):
    '''开叫 1C 后应叫'''
    pt = sum(pts)

    if pt < 4:
        return 0 # Pass
    
    if pt >= 11 and distribute[3] >= 4 and distribute[0] < 4 and distribute[1] < 4 and distribute[2] < 4:
        return 21 # 2C 低花反加叫
    
    if pt >= 4 and pt <= 6 and max(distribute) >= 6:
        # 阻击叫 忽略4阶
        if max(distribute) == distribute[0] and distribute[1] < 4:
            return 24 # 2S
        if max(distribute) == distribute[1] and distribute[0] < 4:
            return 23 # 2H 
        if max(distribute) == distribute[2] and distribute[0] < 4 and distribute[1] < 4:
            return 22 # 2D
    
    if pt >= 4 and pt <= 8 and distribute[3] >= 5 and reset_pt(pts, distribute, 3) < 12:
        return 31 # 3C
    if pt >= 4 and pt <= 8 and distribute[3] >= 5 and reset_pt(pts, distribute, 3) >= 12 and reset_pt(pts, distribute, 3) <= 13:
        return 41 # 4C
    if pt >= 4 and pt <= 8 and distribute[3] >= 5 and reset_pt(pts, distribute, 3) > 13:
        return 51 # 5C

    # Splinter
    if pt >= 11 and distribute[3] >= 5 and distribute[2] <= 1:
        return 32 # 3D
    if pt >= 11 and distribute[3] >= 5 and distribute[1] <= 1:
        return 33 # 3H
    if pt >= 11 and distribute[3] >= 5 and distribute[0] <= 1:
        return 34 # 3S

    if pt >= 6 and distribute[0] < 4 and distribute[1] < 4 and distribute[2] >= 4 and distribute[3] < 5:
        return 12 # 1D
    if pt >= 6 and distribute[0] <= distribute[1] and distribute[1] >= 4:
        if distribute[0] == distribute[1]:
            if pt > 11:
                return 13 # 1H 逆叫
            else:
                return 14 # 1S
        else:
            return 13 # 1H
    if pt >= 6 and distribute[0] >= distribute[1] and distribute[0] >= 4:
        return 14 # 1S
    if pt >= 6 and pt <= 10 and is_balance(distribute):
        return 15 # 1NT
    if pt >= 11 and pt <= 12 and is_balance(distribute):
        return 25 # 2NT 邀请
    if pt >= 13 and is_balance(distribute):
        return 35 # 3NT 
    
    print('r11: unused')
    # 无一步到局

    return 0

def r12(pts:list, distribute:list): 
    '''开叫 1D 后应叫''' 
    pt = sum(pts)
    if pt < 5: 
        return 0 # Pass
    if pt >= 10 and pt < 13 and distribute[2] >= 5 and distribute[0] < 4 and distribute[1] < 4 and distribute[3] < 4: 
        return 22 # 2D 低花反加叫
    if pt >= 4 and pt <= 6 and max(distribute) >= 6:
        # 阻击叫 忽略4阶
        if max(distribute) == distribute[0] and distribute[1] < 4:
            return 24 # 2S
        if max(distribute) == distribute[1] and distribute[0] < 4:
            return 23 # 2H 
        if max(distribute) == distribute[3] and distribute[0] < 4 and distribute[1] < 4:
            return 31 # 3C

    # Splinter
    if pt >= 11 and distribute[2] >= 5 and distribute[3] <= 1:
        return 41 # 4C
    if pt >= 11 and distribute[2] >= 5 and distribute[1] <= 1:
        return 33 # 3H
    if pt >= 11 and distribute[2] >= 5 and distribute[0] <= 1:
        return 34 # 3S

    if pt >= 8 and pt <= 11 and distribute[0] < 4 and distribute[1] < 4 and distribute[3] >= 6 and distribute[2] < 5: 
        return 21 # 2C 

    if pt >= 6 and distribute[0] <= distribute[1] and distribute[1] >= 4: 
        if distribute[0] == distribute[1]: 
            if pt > 11:
                return 13 # 1H 逆叫 
            else: 
                return 14 # 1S 
        else: 
            return 13 # 1H 

    if pt >= 6 and distribute[0] > distribute[1] and distribute[0] >= 4:
        return 14 # 1S 
    if pt >= 6 and pt <= 10 and is_balance(distribute): 
        return 15 # 1NT
    if pt >= 11 and pt <= 12 and is_balance(distribute):
        return 25 # 2NT 邀请
    if pt >= 13 and is_balance(distribute):
        return 35 # 3NT 

    print('r12: unused') 
    # 无一步到局

    return 0

# bid.py
def r13(pts:list, distribute:list):
    '''开叫 1H 后应叫'''
    pt = sum(pts)
    if pt < 5:
        return 0 # Pass
    if pt >= 5 and pt <= 10 and max(distribute) >= 6:
        # 阻击叫
        if max(distribute) == distribute[0] and distribute[1] < 4:
            return min(distribute[0] - 4, 2) * 10 + 4 # 2S 
        if max(distribute) == distribute[1] and distribute[0] < 4:
            return 43 # 4H

    if pt >= 6 and distribute[0] >= 4:
        return 14 # 1S
    
    if pt >= 5 and pt < 12 and distribute[0] < 4:
        return 15 # 1NT
    
    if pt >= 13 and distribute[0] < 4 and distribute[1] < 4:
        # 二盖一逼局
        if distribute[2] < distribute[3] or (distribute[2] == distribute[3] and distribute[3] == 3):
            return 21 # 2C
        return 22 # 2D
    
    # Bergen Raises
    if distribute[1] >= 4 and pt >= 7 and pt <= 9:
        return 31 # 3C
    if distribute[1] >= 4 and pt >= 10 and pt <= 12:
        return 32 # 3D
    
    # Splinter
    if pt >= 13 and distribute[1] >= 4 and is_balance(distribute):
        return 35 # 3NT
    if pt >= 13 and distribute[1] >= 4 and distribute[0] <= 1:
        return 34 # 3S
    if pt >= 13 and distribute[1] >= 4 and distribute[2] <= 1:
        return 42 # 4D
    if pt >= 13 and distribute[1] >= 4 and distribute[3] <= 1:
        return 41 # 4C


    
def r14(pts:list, distribute:list):
    '''开叫 1S 后应叫'''
def r15(pts:list, distribute:list):
    '''开叫 1NT 后应叫'''
def r21(pts:list, distribute:list):
    '''开叫 2C 后应叫'''
def r22(pts:list, distribute:list):
    '''开叫 2D 后应叫'''
def r23(pts:list, distribute:list):
    '''开叫 2H 后应叫'''
def r24(pts:list, distribute:list):
    '''开叫 2S 后应叫'''
def r31(pts:list, distribute:list):
    '''开叫 3C 后应叫'''
def r32(pts:list, distribute:list):
    '''开叫 3D 后应叫'''
def r33(pts:list, distribute:list):
    '''开叫 3H 后应叫'''
def r34(pts:list, distribute:list):
    '''开叫 3S 后应叫'''

def r1112(pts:list, distribute:list):
    ''' 1C - 1D - ? '''
def r1113(pts:list, distribute:list):
    ''' 1C - 1H - ? '''
def r1114(pts:list, distribute:list):
    ''' 1C - 1S - ? '''
def r1213(pts:list, distribute:list):
    ''' 1D - 1H - ? '''
def r1214(pts:list, distribute:list):
    ''' 1D - 1S - ? '''
def r1314(pts:list, distribute:list):
    ''' 1H - 1S - ? '''
def r1115(pts:list, distribute:list):
    ''' 1C - 1NT - ? '''
def r1215(pts:list, distribute:list):
    ''' 1D - 1NT - ? '''
def r1315(pts:list, distribute:list):
    ''' 1H - 1NT - ? '''
def r1415(pts:list, distribute:list):
    ''' 1S - 1NT - ? '''

def r111213(pts:list, distribute:list):
    '''
    1C - 1D -
    1H - ?
    '''
def r111214(pts:list, distribute:list):
    '''
    1C - 1D -
    1S - ? '''
def r121314(pts:list, distribute:list):
    '''
    1D - 1H - 
    1S - ? '''
def r111215(pts:list, distribute:list):
    '''
    1C - 1D - 
    1NT - ? '''
def r111315(pts:list, distribute:list):
    '''
    1C - 1H - 
    1NT - ?
    '''
def r111415(pts:list, distribute:list):
    '''
    1C - 1S -
    1NT - ? '''
def r121315(pts:list, distribute:list):
    '''
    1D - 1H - 
    1NT - ?'''
def r121415(pts:list, distribute:list):
    '''
    1D - 1S - 
    1NT - ? '''
def r131415(pts:list, distribute:list):
    '''
    1H - 1S - 
    1NT - ? '''

