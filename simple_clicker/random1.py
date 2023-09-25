from tkinter import *
import random

tk = Tk()

money = 0

tk.title("심심해서 만든 프로그램")
tk.geometry("640x480")
tk.resizable(False,False)

label = Label(tk, borderwidth= 2, relief='solid', width=30, height=5, font=("맑은 고딕", 16))
label.pack()

def getCoin():
    global money
    n = random.randint(1, 100)
    if n % 100 == 0:
        money += 100
    elif n % 20 == 0:
        money += 20
    elif n % 10 == 0:
        money += 10
    else:
        money += 1
    
    label["text"] = money
    label.update()


btn1 = Button(tk, text="코인 얻기", borderwidth= 1, width= 10, height= 2, command=getCoin)
btn1.pack()

tk.mainloop()