from random import *
from operator import itemgetter
from tkinter import *

SHAPE_TUPLE = ('◆','♠','♥','♣')
RANK_TUPLE = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
#card.py================================================================================================================================
def createDeck():
    deck = []
    for suit in SHAPE_TUPLE:
        for value, rank in enumerate(RANK_TUPLE):
            card = {'suit': suit, 'rank': rank, 'value': value+1, 'hidden': False}
            deck.append(card)
    return deck

def shuffleCards(deck):
    shuffle(deck)
    return deck 

def getCard(deck, hidden = False):
    card = deck.pop() # 맨 뒤에서 한장 제거
    if hidden:
        card['hidden'] = True
    return card

def getCards(deck, numCards, hidden = False):
    cardList = []
    for i in range(numCards):
        card = deck.pop() # 맨 뒤에서 한장 제거
        if hidden:
            card['hidden'] = True
        cardList.append(card)
    return cardList

# 카드 목록을 출력
def printCardList(cardList, hidden = False):
    for i in range(len(cardList)):
        if hidden and cardList[i]['hidden']:
            print(f"{i+1}. This card is HIDDEN.")
        else:
            print(f"{i+1}. {cardList[i]['suit']} {cardList[i]['rank']}")
            
def sortCards(cardList):
    cardList.sort(key=itemgetter('value'))
    return cardList            

def showCards(players, playersCardList, hidden=True, verbose=True):
    
    for player in players:
        print(f">>> {player['name']}의 현재 카드는 다음과 같습니다.")
        printCardList(playersCardList[player['ID']], hidden)
        print()

def dealCards(deck, players, playersCardList, numCards, hidden=False, verbose=True):
    
    if numCards == 1:

        for player in players:
            print(f">>> {player['name']}에게 {numCards}장의 카드를 나누어줍니다.")
            applyHidden = hidden if player['ID'] != "share" else False
            playersCardList[player['ID']] = []
            playersCardList[player['ID']].append(getCard(deck, hidden=applyHidden))
        
    elif numCards > 1:

        for player in players:
            print(f">>> {player['name']}에게 {numCards}장의 카드를 나누어줍니다.")
            playersCardList[player['ID']] = getCards(deck, numCards, hidden)
        
    else:
        print(">>> [ERROR] 최소한 1장 이상 카드를 나누어주어야 합니다!")
        
    return playersCardList

def dealCommunityCards(deck, playersCardList, numCards, hidden=False, verbose=True):
    if numCards <= len(deck):
        print(f">>> {numCards}장의 커뮤니티 카드를 뽑습니다.")
        playersCardList["share"] = getCards(deck, numCards, hidden)
    else:
        print(">>> [ERROR] 카드가 부족하여 커뮤니티 카드를 더 이상 뽑을 수 없습니다!")
        
    return playersCardList
#util.py===============================================================================================================================
# 특정 범위의 정수를 입력받는 함수
def int_get(input_str, minval=1, maxval=None, default=None): 
    
    while True:
        val = input(input_str+'['+str(default)+'] ')
        if val == '' and default is not None:
            return default
        elif set(val) <= set("0123456789"):
            val = int(val)
            if maxval is not None:
                if minval <= val <=maxval:
                    return val
                else:
                    print(">>> [ERROR] 입력값이 범위를 벗어났습니다!")
            else:
                if minval <= val:
                    return val
                else:
                    print(">>> [ERROR] 입력값이 범위를 벗어났습니다!")
        else:
            print(">>> [ERROR] 정수를 입력해주세요!")
#main.py===============================================================================================================================
import time
PLAYERS = ({"ID": "you", "name": "당신"}, {"ID": "dealer", "name": "딜러"})
SHARE = ({"ID": "share", "name": "공유테이블"},)

dealer_index = next((index for index, player in enumerate(PLAYERS) if player["ID"] == "dealer"), None)
my_index = next((index for index, player in enumerate(PLAYERS) if player["ID"] == "you"), None)

def isRoyalStraightFlush(cardList):
    cardList = sortCards(cardList)
    royalstraightflush = ['10', 'J', 'Q', 'K', 'A']
    suits = {card['suit'] for card in cardList}
    if len(suits) == 1:
        ranks = [card['rank'] for card in cardList]
        if ranks == royalstraightflush:
            return True
    return False

def isStraightFlush(cardList):
    cardList = sortCards(cardList)
    suits = {card['suit'] for card in cardList}
    if len(suits) == 1:
        ranks = [card['rank'] for card in cardList]
        for i in range(len(ranks) - 1):
            if RANK_TUPLE.index(ranks[i]) + 1 != RANK_TUPLE.index(ranks[i + 1]):
                return False
        return True
    return False

def isFourOfAKind(cardList):
    cardList = sortCards(cardList)
    for i in range(len(cardList) - 3):
        if cardList[i]['rank'] == cardList[i + 1]['rank'] == cardList[i + 2]['rank'] == cardList[i + 3]['rank']:
            return True
    return False

def isFullHouse(cardList):
    cardList = sortCards(cardList)
    counts = {}
    for card in cardList:
        counts[card['rank']] = counts.get(card['rank'], 0) + 1
    if 2 in counts.values() and 3 in counts.values():
        return True
    return False

def isFlush(cardList):
    suits = [card['suit'] for card in cardList]
    for suit in suits:
        if suits.count(suit) >= 5:
            return True
    return False

def isStraight(cardList):
    cardList = sortCards(cardList)
    for i in range(len(cardList) - 1):
        if RANK_TUPLE.index(cardList[i + 1]['rank']) != RANK_TUPLE.index(cardList[i]['rank']) + 1:
            return False
    return True

def isThreeOfAKind(cardList):
    cardList = sortCards(cardList)
    for i in range(len(cardList) - 2):
        if cardList[i]['rank'] == cardList[i + 1]['rank'] == cardList[i + 2]['rank']:
            return True
    return False

def isTwoPair(cardList):
    cardList = sortCards(cardList)
    pairs = []
    for i in range(len(cardList) - 1):
        if cardList[i]['rank'] == cardList[i + 1]['rank']:
            pairs.append(cardList[i]['value'])
    if len(pairs) >= 2:
        return pairs
    return None

def isOnePair(cardList):
    cardList = sortCards(cardList)
    for i in range(len(cardList) - 1):
        if cardList[i]['rank'] == cardList[i + 1]['rank']:
            return True
    return False

def isHighCard(cardList):
    cardList = sortCards(cardList)
    high = cardList[-1]['value']
    
    return high

RANKING = ({"func": isRoyalStraightFlush,    "name": "로열 스트레이트 플러시" }, 
           {"func": isStraightFlush, "name": "스트레이트 플러시" }, 
           {"func": isFourOfAKind,   "name": "포카드" }, 
           {"func": isFullHouse,   "name": "풀하우스" }, 
           {"func": isFlush,   "name": "플러시" }, 
           {"func": isStraight,    "name": "스트레이트" }, 
           {"func": isThreeOfAKind,     "name": "트리플" },
           {"func": isTwoPair,  "name": "투페어"},
           {"func": isOnePair,  "name": "원페어"},
           {"func": isHighCard, "name": "탑"})

#GUI.py=============================================================================================================================================================
window = Tk()

window.title("텍사스 홀덤")
window.geometry("1440x720")
window.resizable(False, False)

def process1():
    global go_button2
    sharelabel_1 = Label(window, relief='solid', width= 12, height= 10)
    sharelabel_1.place(x=400, y= 280)
    sharelabel_1.config(text=f"{playersCardList['share'][0]['suit']} {playersCardList['share'][0]['rank']}")
    go_button1.destroy()
    go_button2 = Button(window, text="콜/쿼터/삥/레이즈", width=15, height=3, command= process2)
    go_button2.place(x=250, y=600)
    

def process2():
    global go_button3
    sharelabel_2 = Label(window, relief='solid', width= 12, height= 10)
    sharelabel_2.place(x=535, y= 280)
    sharelabel_2.config(text=f"{playersCardList['share'][1]['suit']} {playersCardList['share'][1]['rank']}")
    go_button2.destroy()
    go_button3 = Button(window, text="콜/쿼터/삥/레이즈", width=15, height=3, command=process3)
    go_button3.place(x=250, y=600)

def process3():
    global go_button4
    sharelabel_3 = Label(window, relief='solid', width= 12, height= 10)
    sharelabel_3.place(x=670, y= 280)
    sharelabel_3.config(text=f"{playersCardList['share'][2]['suit']} {playersCardList['share'][2]['rank']}")
    go_button3.destroy()
    go_button4 = Button(window, text="콜/쿼터/삥/레이즈", width=15, height=3, command=process4)
    go_button4.place(x=250, y=600)
    
def process4():
    global go_button5
    sharelabel_4 = Label(window, relief='solid', width= 12, height= 10)
    sharelabel_4.place(x=805, y= 280)
    sharelabel_4.config(text=f"{playersCardList['share'][3]['suit']} {playersCardList['share'][3]['rank']}")
    go_button4.destroy()
    go_button5 = Button(window, text="콜/쿼터/삥/레이즈", width=15, height=3, command=process5)
    go_button5.place(x=250, y=600)
    
def process5():
    global go_button6
    sharelabel_5 = Label(window, relief='solid', width= 12, height= 10)
    sharelabel_5.place(x=940, y= 280)
    sharelabel_5.config(text=f"{playersCardList['share'][4]['suit']} {playersCardList['share'][4]['rank']}")
    go_button5.destroy()
    go_button6 = Button(window, text="결과 보기", width=15, height=3, command=process6)
    go_button6.place(x=250, y=600)

def checkRanking(playersCardList):
    global playersRanking
    playersRanking = []
    for player in PLAYERS:
        for i, rank in enumerate(RANKING):
            allCards = playersCardList[player['ID']] + playersCardList['share']
            result = rank["func"](allCards)
            if result:
                high_card_value = None
                if isinstance(result, list):  # Check if high card value is returned
                    high_card_value = result
                playersRanking.append({"playerID": player['ID'], "rankID": i, "high": high_card_value})
                break
    return playersRanking

def whoWin(playersRanking):
    global winID
    winRank = len(RANKING)
    winHigh = 1
    winID = []
    for i, rank in enumerate(playersRanking):
        if (rank["rankID"] < winRank) or (rank["rankID"] == winRank and rank["high"] is not None and (rank["high"] > winHigh)):
            winID.clear()
            winID.append(i)
            winRank = rank["rankID"]
            winHigh = rank["high"]
        elif (rank["rankID"] == winRank) and (rank["high"] == winHigh): 
            if rank["rankID"] == RANKING.index({"func": isOnePair, "name": "원페어"}):
                winID.append(i)
            elif rank["rankID"] == RANKING.index({"func": isTwoPair, "name": "투페어"}):
                # Compare the higher pair
                if playersRanking[i]["high"][0] > playersRanking[winID[0]]["high"][0]:
                    winID.clear()
                    winID.append(i)
                elif playersRanking[i]["high"][0] == playersRanking[winID[0]]["high"][0]:
                    # Compare the lower pair
                    if playersRanking[i]["high"][1] > playersRanking[winID[0]]["high"][1]:
                        winID.clear()
                        winID.append(i)
            elif rank["rankID"] in [RANKING.index(r) for r in [{"func": isThreeOfAKind, "name": "트리플"}, 
                                                              {"func": isFourOfAKind, "name": "포카드"}]]:
                # Compare the triple or quadruple
                if playersRanking[i]["high"] > playersRanking[winID[0]]["high"]:
                    winID.clear()
                    winID.append(i)
            elif rank["rankID"] in [RANKING.index(r) for r in [{"func": isStraight, "name": "스트레이트"}, 
                                                              {"func": isFlush, "name": "플러시"},
                                                              {"func": isFullHouse, "name": "풀하우스"},
                                                              {"func": isStraightFlush, "name": "스트레이트 플러시"},
                                                              {"func": isRoyalStraightFlush, "name": "로열 스트레이트 플러시"}]]:
                # Compare the highest card
                if playersRanking[i]["high"] > playersRanking[winID[0]]["high"]:
                    winID.clear()
                    winID.append(i)
    
    return winID

def process6():
    global winID
    playersRanking = checkRanking(playersCardList)
    winID = whoWin(playersRanking)  # 이 부분에서 winID를 전역 변수로 선언하겠습니다.
    
    winner_names = [PLAYERS[rank["playerID"]]["name"] for rank in playersRanking if rank["playerID"] in winID]  # winner_names를 새로 계산합니다.
    
    result_ui = Toplevel(window)
    result_ui.title("결과 발표")
    result_ui.geometry("320x160")
    result_ui.resizable(False, False)

    result_label = Label(result_ui, width=50, height=3, font=("맑은 고딕", 16))
    result_label.pack()

    if 0 in winID:
        if len(winID) > 1:
            result_label.config(text="비겼습니다.") # draw
        else:
            result_label.config(text="당신이 이겼습니다.") # win or defeat
    else:
        result_label.config(text="상대가 이겼습니다.") # defeat or win

    dealer_card_left.config(text=f"{playersCardList['dealer'][0]['suit']} {playersCardList['dealer'][0]['rank']}")
    dealer_card_right.config(text=f"{playersCardList['dealer'][1]['suit']} {playersCardList['dealer'][1]['rank']}")

    if len(winner_names) > 0:
        dealer_rank_label = Label(window, text=f"{winner_names[0]}", width=50, height=3, font=("맑은 고딕", 16))
        dealer_rank_label.place(x=400, y=150)

        my_rank_label = Label(window, text=f"{winner_names[0]}", width=50, height=3, font=("맑은 고딕", 16))
        my_rank_label.place(x=400, y=470)
        
    # 딜러(상대)의 족보 확인 및 라벨 생성
    opponent_rank_label = Label(window, text=f"{RANKING[playersRanking[1]['rankID']]['name']}", width=50, height=3, font=("맑은 고딕", 16))
    opponent_rank_label.place(x=400, y=150)
    
    # 나의 족보 확인 및 라벨 생성
    mine_rank_label = Label(window, text=f"{RANKING[playersRanking[0]['rankID']]['name']}", width=50, height=3, font=("맑은 고딕", 16))
    mine_rank_label.place(x=400, y=470)

def play_game():
    global deck, go_button1, playersCardList, dealer_card_left, dealer_card_right
    deck = createDeck()
    deck = shuffleCards(deck)
    
    playersCardList = dealCards(deck, PLAYERS, {}, 2, hidden=True)
    
    mylabel = Label(window, text=f"나 자신", font=("맑은 고딕", 16))
    mylabel.place(x=670, y= 670)
    dealerlabel = Label(window, text=f"상대", font=("맑은 고딕", 16))
    dealerlabel.place(x=680, y=20)
    my_card_left = Label(window, width=6, height=5, relief='solid', text=f"{playersCardList['you'][0]['suit']} {playersCardList['you'][0]['rank']}")
    my_card_left.place(x= 650, y= 580)
    my_card_right = Label(window, width=6, height=5, relief='solid', text=f"{playersCardList['you'][1]['suit']} {playersCardList['you'][1]['rank']}")
    my_card_right.place(x= 710, y= 580)
    dealer_card_left = Label(window, relief='solid', width=6, height=5, text="hidden")
    dealer_card_left.place(x=650, y= 60)
    
    dealer_card_right = Label(window, relief='solid', width=6, height=5, text="hidden")
    dealer_card_right.place(x=710, y= 60)
    
    playersCardList = dealCommunityCards(deck, playersCardList, 5, hidden=False)
    go_button1 = Button(window, text="콜/쿼터/삥/레이즈", width=15, height=3, command=process1)
    go_button1.place(x=250, y=600)
    
play_game()

window.mainloop()