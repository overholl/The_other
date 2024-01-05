import tkinter as tk
import random as rd
import time

window = tk.Tk()

score = 0
win_count = 0

enemy_hp = 100
my_hp = 100

window.geometry("640x480")
window.title("Random Battle")
window.resizable(False,False)

label = tk.Label(window, text="상대", width=15, height=3, font=("맑은 고딕", 20))
label.pack()

enemylabel = tk.Label(window, width=20, height=2, relief='solid', borderwidth= 2, font=("맑은 고딕", 16), text="100")
enemylabel.pack()
mylabel = tk.Label(window, width=20, height=2, relief='solid', borderwidth= 2, font=("맑은 고딕", 16), text="100")
mylabel.place(x=200, y=300)
playerlabel = tk.Label(window, text="플레이어", width=10, height=1, font=("맑은 고딕", 20))
playerlabel.place(x=240, y=380)

winlabel = tk.Label(window, text=f"win_count=0", font=("맑은 고딕", 10), width=15, height=2)
winlabel.place(x=1, y=20)

slabel = tk.Label(window, text=f"score=0", font=("맑은 고딕", 10), width=15, height=2)
slabel.place(x=530, y=20)

def randomdamage():
    global enemy_hp, score, win_count, my_hp
    n = rd.randint(1,10)
    enemy_hp -= n
    score += n*10
    if enemy_hp <= 0:
        enemy_hp = 100
        win_count +=1
        my_hp = 100
    winlabel.config(text=f"win_count={win_count}")
    slabel.config(text=f"score={score}")
    enemylabel["text"] = enemy_hp
    enemylabel.update()
    
def enemyturn():
    global my_hp, score, win_count, enemy_hp
    n = rd.randint(1,10)
    my_hp -= n
    if my_hp <=0:
        showdead = tk.Toplevel(window)
        showdead.title("Game Over")
        showdead.geometry("640x480")
        resultframe = tk.Label(showdead, text="죽으셨습니다.\n 적의 남은 체력:" + str(enemy_hp) + "\n 점수:" + str(score) + "\n 적을 물리친 횟수:" + str(win_count))
        showdead.resizable(False,False)
        resultframe.pack()
    mylabel["text"] = my_hp
    mylabel.update()

def processing_game():
    randomdamage()
    time.sleep(2)
    enemyturn()

def tutorial():
    tt = tk.Toplevel(window)
    tt.geometry("640x480")
    tt.title("튜토리얼")
    tlb = tk.Label(tt, text="Random Battle에 오신 걸 환영합니다.\n이 게임의 설명을 해 드리겠습니다.\n기본적으로 각자 100의 HP가 주어집니다.\n중앙에 게임 진행하기라는 버튼을 누르면 시작이 되며\n각자 1~10 사이의 값중 랜덤으로 HP가 줄어듭니다.\n적의 HP를 0이하가 되면 양쪽 다 체력이 100으로 처리되며, 적을 쓰러뜨린 것이므로\n왼쪽 상단 win_count가 오릅니다.\n스코어는 적에게 입힌 데미지에 따라 주어집니다.", font=('맑은 고딕', 12))
    tt.resizable(False,False)
    tlb.pack()

def confirm(ntbx):
    nick = ntbx.get()
    playerlabel.configure(text=nick)

def change_nickname():
    nt = tk.Toplevel(window)
    nt.title("닉 바꾸기")
    nt.geometry("320x240")
    ntbx = tk.Entry(nt, width=30)
    ntbx.grid(column=0, row=0)
    ntbtn = tk.Button(nt, text="확인", command=lambda: confirm(ntbx))
    ntbtn.grid(column=0, row=1)

btn = tk.Button(window, text="게임 진행하기", borderwidth= 1, width= 20, height= 3, command= processing_game)
btn.place(x=250, y= 210)

nickbtn = tk.Button(window, text="닉 바꾸기", borderwidth= 1, width= 10, height= 2, command= change_nickname)
nickbtn.place(x=100, y= 380)

menu = tk.Menu(window)
menu1 = tk.Menu(menu, tearoff=0)
menu1.add_command(label="튜토리얼", command=tutorial)
menu.add_cascade(label='소개', menu=menu1)
window.config(menu=menu)

menu2 = tk.Menu(menu, tearoff=0)
menu2.add_command(label='종료', command=window.destroy)
menu.add_cascade(label='종료', menu=menu2)
window.config(menu=menu)

if __name__ == "__main__":
    window.mainloop()