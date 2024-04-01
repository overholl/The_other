from tkinter import *
from random import *
from math import *

defalut_money = int(1000)
current_money = defalut_money

betting_money = int(0)

def pick():
    return choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

window = Tk()
window.title("슬롯 머신")
window.geometry("640x480")
window.resizable(False,False)

main_label = Label(window, borderwidth= 2, relief='solid', width=30, height=5, font=("맑은 고딕", 16))
main_label.place(x= 150, y= 50)

current_money_label = Label(window, text=f"플레이어가 현재 가진 돈: {defalut_money}", font=("맑은 고딕", 10))
current_money_label.place(x= 400, y= 20)

bml = Label(window, text=f"플레이어가 베팅한 돈: 0", font=("맑은 고딕", 10))
bml.place(x=1, y=20)

def comfirm(event):
    global current_money, betting_money
    betting_money = int(betting_money_size.get())
    if int(betting_money) > 0 and int(betting_money) <= int(current_money):
        bml.configure(text=f"플레이어가 베팅한 돈: {betting_money}")
        current_money = current_money - int(betting_money)
        current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
        betting_scene.destroy()
        return betting_money
    else:
        ValueErrorMessage = Toplevel(betting_scene)
        ValueErrorMessage.title("값이 옳지 않습니다.")
        ValueErrorMessage.geometry("320x160")
        ValueErrorMessage.resizable(False,False)
        errormessage = Label(ValueErrorMessage, text="돈이 없거나, 베팅한 돈이 없거나 음수입니다.")
        errormessage.pack()

def ALL_IN(event):
    global betting_scene, current_money, betting_money
    betting_money = current_money
    bml.configure(text=f"플레이어가 베팅한 돈: {betting_money}")
    current_money -= betting_money
    current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
    betting_scene.destroy()
    return betting_money

def Three_Quarters(event):
    global betting_scene, current_money, betting_money
    betting_money = round(current_money * 0.75)
    bml.configure(text=f"플레이어가 베팅한 돈: {betting_money}")
    current_money -= betting_money
    current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
    betting_scene.destroy()
    return betting_money

def half_betting(event):
    global betting_scene, current_money, betting_money
    betting_money = round(current_money / 2)
    bml.configure(text=f"플레이어가 베팅한 돈: {betting_money}")
    current_money -= betting_money
    current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
    betting_scene.destroy()
    return betting_money

def One_Quarters(event):
    global betting_scene, current_money, betting_money
    betting_money = round(current_money / 4)
    bml.configure(text=f"플레이어가 베팅한 돈: {betting_money}")
    current_money -= betting_money
    current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
    betting_scene.destroy()
    return betting_money

def betting():
    global betting_scene, betting_money_size
    betting_scene = Toplevel(window)
    betting_scene.geometry("480x320")
    betting_scene.resizable(False, False)
    betting_scene.title("베팅 창")
    
    betting_money_size = Entry(betting_scene, width = 65)
    betting_money_size.grid(row=0, columnspan=5, sticky=E + W)
    betting_money_button = Button(betting_scene, text="금액 결정",borderwidth= 1, width= 10, height= 2)
    betting_money_button.grid(row=1, column=0, sticky=E + W)
    betting_money_button.bind('<Button-1>', comfirm)
    
    betting_all_in_button = Button(betting_scene, text="올 인",borderwidth= 1, width= 10, height= 2)
    betting_all_in_button.grid(row=1, column=1, sticky=E + W)
    betting_all_in_button.bind('<Button-1>', ALL_IN)
    
    betting_three_quarters = Button(betting_scene, text="3/4 베팅",borderwidth= 1, width= 10, height= 2)
    betting_three_quarters.grid(row=1, column=2, sticky=E + W)
    betting_three_quarters.bind('<Button-1>', Three_Quarters)
    
    betting_half_money_button = Button(betting_scene, text="절반 베팅",borderwidth= 1, width= 10, height= 2)
    betting_half_money_button.grid(row=1, column=3, sticky=E + W)
    betting_half_money_button.bind('<Button-1>', half_betting)
    
    betting_one_quarters = Button(betting_scene, text="1/4 베팅",borderwidth= 1, width= 10, height= 2)
    betting_one_quarters.grid(row=1, column=4, sticky=E + W)
    betting_one_quarters.bind('<Button-1>', One_Quarters)
   
def play_slot():
    global current_money, betting_money
    if betting_money == 0:
        ValueErrorMessage = Toplevel(window)
        ValueErrorMessage.title("값이 옳지 않습니다.")
        ValueErrorMessage.geometry("320x160")
        ValueErrorMessage.resizable(False,False)
        errormessage = Label(ValueErrorMessage, text="베팅할 돈을 입력하세요.")
        errormessage.pack()
        return
    
    left_number = pick()
    middle_number = pick()
    right_number = pick()
    main_label.config(text=f"{left_number}  {middle_number}  {right_number}")
    
    if left_number == middle_number == right_number:
        current_money += betting_money * 10
        betting_money = 0
        current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
        bml.config(text=f"플레이어가 베팅한 돈: {betting_money}")
        return current_money, betting_money
    elif left_number == middle_number or middle_number == right_number or left_number == right_number:
        current_money += betting_money * 2
        betting_money = 0
        current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
        bml.config(text=f"플레이어가 베팅한 돈: {betting_money}")
        return current_money, betting_money
    else:
        current_money += round(betting_money * 0.5)
        betting_money = 0
        current_money_label.config(text=f"플레이어가 현재 가진 돈: {current_money}")
        bml.config(text=f"플레이어가 베팅한 돈: {betting_money}")
        return current_money, betting_money

def game_exit():
    gameover.destroy()
    window.destroy()

betting_button = Button(window, text="베팅하기", borderwidth= 1, width= 15, height= 3, highlightthickness= 1, command=betting)
betting_button.place(x= 219, y= 207)

def NO_MONEY():
    global gameover, gameover_label, gameover_button
    gameover = Toplevel(window)
    gameover.title("게임 오버")
    gameover.resizable(False, False)
    gameover.geometry("640x480")
    gameover_label = Label(gameover, text="게임 오버!", font=("맑은 고딕",32))
    gameover_label.pack()
    gameover_button = Button(gameover, text="종료하기", borderwidth= 1, width= 15, height= 3, highlightthickness= 1, command=game_exit)
    gameover_button.pack()

play_slot_button = Button(window, text="슬롯 돌리기", borderwidth= 1, width= 15, highlightthickness=1, height= 3, command=play_slot)
play_slot_button.place(x=333, y=207)

no_money = Button(window, text="돈이 없어요?", borderwidth= 1, width= 15, highlightthickness=1, height= 3, command=NO_MONEY)
no_money.place(x=278, y=361)

window.mainloop()