import numpy as np
from ai import ai
from TicTacToe import TicTacToe
import time

uses  = np.load('uses.npy').flatten()
wins  = np.load('wins.npy').flatten()
AI_x    = ai(uses, wins, 0)
AI_o    = ai(uses, wins, 0)

# game.run()


for i in range(10):
    state = [0] * 9
    t = 0
    game = TicTacToe()
    while game.end_code < 0:
        if (t+1)%2 == 0:
            move     = AI_x.get_action(state, t)
            state[t] = move
            game.fill_pos(move)
            t += 1

        game.update()
        game.progress = False
        if game.end_code <0:
            while game.progress == False:
                game.update()
                time.sleep(0.0167)
            t += 1
            state[t] = game.last_move
    game.terminate()
    AI_o.update_mem('uses.npy', 'wins.npy', game.end_code, state, t)

