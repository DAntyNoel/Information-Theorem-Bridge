def read_cards(s:str):
    suits=s.split('.')
    structure=[len(suits[0]),len(suits[1]),len(suits[2]),len(suits[3])]
    hcp=0
    for suit in suits:
        for card in suit:
            if card=='A':hcp+=4
            elif card=='K':hcp+=3
            elif card=='Q':hcp+=2
            elif card=='J':hcp+=1
    return (structure,hcp)
class bid_agent1:
    def __init__(self,card_information) -> None:
        self.struct=card_information[0]
        self.hcp=card_information[1]
        self.target=0#0部分定约，1成局定约,2小满贯,3大满贯
        self.partner_eva=[0,21]
    def bid(self,process):
        if process[-1]==4:
            self.partner_eva=[12,21]
            if self.hcp<6:return 0
            elif self.hcp<10:return 9
            elif self.hcp<13:return 14
            elif self.hcp<18:return 19
        elif 
def transfer(s:str):
    number=str(int((s-1)/5)+1)
    suit=s%5
    if s==0:return number+'NT'
    elif s==1:return number+'S'
    elif s==1:return number+'H'
    elif s==1:return number+'D'
    elif s==1:return number+'C'
if __name__=='__main__':
    file_name="a.txt"
    f=open(file_name)
    games=f.readlines()
    for game in games:
        cards=game[2:len(game)].split(' ')
        player_card1=read_cards(cards[0])
        player_card2=read_cards(cards[2])
        N_agent=bid_agent1(player_card1)
        S_agent=bid_agent1(player_card2)
        process=[4]
        while(1):
            bid_type=S_agent.bid(process)
            if bid_type==0:
                print(transfer(process[-1]))
                break
            
            
    
    