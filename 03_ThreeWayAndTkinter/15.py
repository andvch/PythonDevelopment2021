#!/usr/bin/env python3
'''
Пятнашки на Tkinter

15.py [N] [--easy-win]

N            - размерность поля, по умолчанию 4
--easy-win   - простая начальная расстановка расстановка
'''

import sys
import random
import tkinter as tk
import tkinter.messagebox

n = 4
easyWin = False

for arg in sys.argv[1:]:
    if arg.isdigit():
        n = int(arg)
    if arg == "--easy-win":
        easyWin = True

board = list(range(n**2))
numButtons = list()

def new():
    global board, easyWin
    random.shuffle(board)
    if easyWin:
        board = list(range(1, n**2 - n + 1)) + [0] + list(range(n**2 - n + 1, n**2))
        easyWin = False
    for i in range(n**2):
        if board[i]:
            numButtons[board[i] - 1].setPos(i)

def checkWin():
    if board[:-1] == list(range(1, n**2)):
        tk.messagebox.showinfo(message="You win!")
        new()

class NumButton(tk.Button):
    def __init__(self, parent, text):
        tk.Button.__init__(self, parent, text=text, command=self.callback)

    def callback(self):
        info = self.grid_info()
        x, y = info["row"], info['column']
        for xNew, yNew in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]:
            i = self.xy2num(xNew, yNew)
            if i != None and board[i] == 0:
                self.setPos(i)
                j = self.xy2num(x, y)
                board[i], board[j] = board[j], board[i]
                checkWin()

    def setPos(self, i):
        self.grid(row=i // n, column=i % n, sticky="NEWS")

    def xy2num(self, x, y):
        return x * n + y if x >= 0 and x < n and y >= 0 and y < n else None

W = tk.Tk()
W.title(str(n**2 - 1))
W.rowconfigure(1, weight=1)
W.columnconfigure(0, weight=1)

head = tk.Frame(W)
head.grid(sticky="EW")
head.columnconfigure(0, weight=1)
head.columnconfigure(1, weight=1)
tk.Button(head, text="New", command=new).grid(row=0, column=0)
tk.Button(head, text="Exit", command=W.quit).grid(row=0, column=1)

body = tk.Frame(W)
body.grid(sticky="NEWS")

for i in range(n):
    body.rowconfigure(i, weight=1)
    body.columnconfigure(i, weight=1)

for i in range(1, n**2):
    numButtons.append(NumButton(body, str(i)))

new()
W.mainloop()
