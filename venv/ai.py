# Vocab:
# DPF = the dimensions of a given play field, in this case 9 because there's a total of 9 moves
import math
import numpy as np
import random


class ai:
    def __init__(self, uses, wins, beta):
        self.uses = uses
        self.wins = wins
        self.beta = beta * 100


    # Receives play field and returns the location of that index within the possible play field 1d matrix.
    #   'Play field': given a game with 4 moves, non-replacing, there are 4! possible variations of moves
    #   this will be represented by [1,0,0,0] matrix for choosing the second square on the first time-step.
    #   get_index simplifies the function and allows for easy 1d 'simulation' for multi-dimension matrix space
    #   in this case, a 1d matrix of length 24 (4!) that simulates a [4,3,2,1] matrix for easy indexing and editing.
    def get_index(self, state):
        index  = 0
        length = len(state)                                        # Degree of play field (DPF)
        for i in range(length):
            index = index + math.factorial(length-(i+1))*state[i]  # sum{(DPF-(i+1))!(x_i)} from i=1 to DPF
        return index                                               # x_i = the number in play field at index i


    # A function that takes in the memory of uses and wins, and calculates the associated state-value with each possible
    # move for a given game state. Takes in uses and wins (A record of all possible game situations), state (game state
    # including the current board), and time t which refers to the move since beginning of the game
    def get_value(self, state, t):
        # Pulls from memory and computes the value of a given state_test (DPF in length)
        def value(state_test):
            index = self.get_index(state_test)
            val_t = self.wins.item(index)/float(self.uses.item(index))   # number of wins/number of uses
            return val_t

        t         = t               # t-1 because the item in index 0 of the state is the move for time point 1 (simplicity)
        num_moves = len(state) - t  # number of potential moves: for t=1 (t=0 ^) and DPF 9, 9-0 = 9 possible moves
        val       = [0]*num_moves   # A matrix to keep track of value's result
        for i in range(num_moves):  # Iterates through all possible moves and stores the values of each in val
            state[t]  = i
            val[i]    = value(state)

        tot = sum(val)
        for i in range(num_moves):  # Normalizes the value variable val (to make it a probability of winning)
            val[i] = val[i]/float(tot)
        return val

    # returns an action based off of either exploitation (maximum value move) or exploration (random move), returns
    # the adjusted move. for example, the first position available move it will return 0 and t-1 for the last.
    def get_action(self, state, t):
        value = self.get_value(state, t)
        if self.beta <= random.randint(0, 100):   # if the random value is less than beta it explores, if not exploit
            test     = max(value)
            num_max  = [0]*len(value)
            for i in range(len(value)):
                if test == value[i]:
                    num_max[i] = 1
            index = np.nonzero(num_max)
            index = index[0]
            if len(num_max) > 1:
                return random.choice(index)       # if there are multiple maximums then choose randomly
            else:
                return index[0]
        else:
            return random.choice(range(len(value)))

    # updates the uses and wins memory, and then saves that file after each game
    def update_mem(self, uses_filename, wins_filename, end_code, end_state, end_time):
        temp = [0]*len(end_state)
        for i in range(end_time):
            temp[i]     = end_state[i]                        # progressively updating state 'replay'
            index       = self.get_index(temp)
            self.uses[index] = self.uses[index] + 1           # updates index for uses regardless of winner

            # will add one to wins for ever even state if O (end_code = 2) wins, and vice-versa
            if end_code == 1 and (i+1) % 2 == 1:
                self.wins[index] = self.wins[index] + 1
            elif end_code == 2 and (i+1) % 2 == 0:
                self.wins[index] = self.wins[index] + 1

        np.save(uses_filename, self.uses)
        np.save(wins_filename, self.wins)
