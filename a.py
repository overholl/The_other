import calendar
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter.filedialog import *
import os
import csv
import pandas as pd

class CalendarApp():
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar with Memo")
        self.root.geometry("600x400")

        # 현재 날짜 정보 가져오기
        self.year = tk.IntVar()
        self.month = tk.IntVar()
        self.day = tk.IntVar()
        self.today = tk.StringVar()

        self.get_today()

        # 날짜 선택 프레임
        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack()

        # 년, 월 선택 위젯
        self.year_entry = tk.Entry(self.frame_top, textvariable=self.year, width=6)
        self.year_entry.pack(side=tk.LEFT, padx=10)
        self.month_entry = tk.Entry(self.frame_top, textvariable=self.month, width=4)
        self.month_entry.pack(side=tk.LEFT, padx=5)

        # 현재 날짜 표시 레이블
        self.today_label = tk.Label(self.frame_top, textvariable=self.today)
        self.today_label.pack(side=tk.RIGHT, padx=10)

        # 캘린더 프레임
        self.frame_calendar = tk.Frame(self.root)
        self.frame_calendar.pack()

        # 달력 그리기
        self.draw_calendar()

    def get_today(self):
        now = datetime.now()
        self.year.set(now.year)
        self.month.set(now.month)
        self.day.set(now.day)
        self.today.set(now.strftime("%Y-%m-%d"))

    def draw_calendar(self):
        # 현재 년, 월의 달력 가져오기
        cal = calendar.monthcalendar(self.year.get(), self.month.get())

        # 달력에 버튼 추가
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    button = tk.Button(
                        self.frame_calendar,
                        text=str(day),
                        command=lambda d=day: self.show_memo_dialog(d),
                    )
                    button.grid(row=week_num, column=day_num, padx=5, pady=5)

    def show_memo_dialog(self, day):
        #각 메뉴가 클릭됐을 때 실행될 함수 정의
        
        #프로그램 정보
        #def about():
        #    label = messagebox.showinfo("About", "메모장 프로그램")
        
        #새 파일
        def new_file():
            #텍스트 영역 지우기
            text_area.delete(1.0, tk.END)
    
        #저장
        def save_file():
            #파일 저장 물어보기
            file = asksaveasfile(mode='w', defaultextension='.txt', filetypes=[('Text files', '.txt')])
            if file != None:
                text = text_area.get(1.0, tk.END+'-1c')
                file.write(text)
                file.close()
    
        #만든 이
        def maker():
            #새 창 만들고 내용 적기
            help_view = tk.Toplevel(memo_dialog)
            help_view.geometry('300x50+850+400')
            help_view.title('만든 이')
            lb = tk.Label(help_view, text='응애')
            lb.pack()
        
        #파일 불러오기
        def open_file():
            try:
                file = askopenfile(parent=memo_dialog, mode='r')
                if file != None:
                    text = file.read()
                    text_area.insert('1.0', text)
                    file.close
            except UnicodeDecodeError:
                    error = tk.Toplevel(memo_dialog)
                    error.geometry('300x50+850+400')
                    error.title('확장자 에러')
                    elb = tk.Label(error, text='지원하지 않는 확장자 입니다.\n.txt파일로 열어주세요.')
                    elb.pack()
            
        #def csv_to_text(file_path):
        #    dt = ""
        #    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        #        csv_reader = csv.reader(csv_file)
        #        
        #        for row in csv_reader:
        #            dt += '\t'.join(row) + '\n'
        #    return dt
        
                       
        # 메모 다이얼로그 표시
        memo_dialog = tk.Toplevel(self.root)
        memo_dialog.title(f"Memo for {self.year.get()}-{self.month.get()}-{day}")
        memo_dialog.geometry('400x400+800+300')
        
        # 메모 메뉴 만들기
        
        # 메뉴 생성
        menu = tk.Menu(memo_dialog)
        
        # 첫번째 메뉴 만들기
        menu_1 = tk.Menu(menu, tearoff=0)
        # 첫번째 메뉴의 세부 메뉴 추가, 함수 연결
        menu_1.add_command(label= '새 파일', command=new_file)
        menu_1.add_command(label= '저장', command=save_file)
        menu_1.add_command(label= '불러오기', command=open_file)
        #줄 추가
        menu_1.add_separator()
        menu_1.add_command(label= '종료', command=memo_dialog.destroy)
        #메뉴바에 추가
        menu.add_cascade(label= '파일',menu=menu_1)
        
        #두번째 메뉴 만들기
        menu_2 = tk.Menu(menu, tearoff=0)
        #세부 메뉴 추가, 함수 연결
        menu_2.add_command(label= '만든 이', command=maker)
        #메뉴바에 추가
        menu.add_cascade(label= '정보', menu=menu_2)
        
        #텍스트 창 만들기
        text_area = tk.Text(memo_dialog)
        #공백설정
        memo_dialog.grid_rowconfigure(0, weight=1)
        memo_dialog.grid_columnconfigure(0, weight=1)
        #화면배치 모두 동서남북 붙인다.
        text_area.grid(sticky = N+E+S+W)
        
        #메뉴구성
        memo_dialog.config(menu=menu)
        memo_dialog.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
