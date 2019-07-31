"""
TicTacToe.py

Author: Joseph Canning

"""

from tkinter import *
from tkinter import font

class TicTacToe:

    def __init__(self):
        self.window = Tk()
        self.frame = Frame()
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.move = 0
        self.end_code = -1
        self.isP1 = True
        self.progress = False
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                button = Button(self.window, text='', width=8, height=4, activebackground='white', bg='grey',
                                font=font.Font(family='System', size=24, weight='bold'),
                                command=lambda row=r,column=c: self.onPress(row=row, column=column))
                button.grid(row=r, column=c)
                self.board[r][c] = button

    def onPress(self, row, column):
        if self.board[row][column] is None or self.board[row][column].cget('text') == 'X' or self.board[row][column].cget('text') == 'O':
            return
        if self.isP1 == True:
            self.board[row][column].config(text='X')
        else:
            self.board[row][column].config(text='O')
        self.isP1 = not self.isP1
        self.evalWinner()
        self.move += 1
        self.progress = True

        self.last_move = self.state.index(row * 3 + column)
        del self.state[self.last_move]

    def evalWinner(self):
        print(self.move)
        if self.move >= 8:
            self.endGame('-')
        for i in range(len(self.board)):
            if self.board[i][0].cget('text') == 'X' and self.board[i][1].cget('text') == 'X' and self.board[i][2].cget('text') == 'X':
                self.endGame('X')
            elif self.board[i][0].cget('text') == 'O' and self.board[i][1].cget('text') == 'O' and self.board[i][2].cget('text') == 'O':
                self.endGame('O')
            elif self.board[0][i].cget('text') == 'X' and self.board[1][i].cget('text') == 'X' and self.board[2][i].cget('text') == 'X':
                self.endGame('X')
            elif self.board[0][i].cget('text') == 'O' and self.board[1][i].cget('text') == 'O' and self.board[2][i].cget('text') == 'O':
                self.endGame('O')
        if self.board[0][0].cget('text') == 'X' and self.board[1][1].cget('text') == 'X' and self.board[2][2].cget('text') == 'X':
            self.endGame('X')
        elif self.board[0][0].cget('text') == 'O' and self.board[1][1].cget('text') == 'O' and self.board[2][2].cget('text') == 'O':
            self.endGame('O')
        elif self.board[0][2].cget('text') == 'X' and self.board[1][1].cget('text') == 'X' and self.board[2][0].cget('text') == 'X':
            self.endGame('X')
        elif self.board[0][2].cget('text') == 'O' and self.board[1][1].cget('text') == 'O' and self.board[2][0].cget('text') == 'O':
            self.endGame('O')

    def endGame(self, winner):
        if winner == '-':
            self.end_code = 0
        elif winner == 'X':
            self.end_code = 1
        elif winner == 'O':
            self.end_code = 2

    def fill_pos(self, stateIndex):
        pos = self.state[stateIndex]
        self.onPress(pos // 3, pos % 3)


    def terminate(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()

    def update(self):
        self.window.update()