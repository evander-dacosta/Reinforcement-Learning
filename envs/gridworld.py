#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 10:40:30 2017

@author: evander
"""

import numpy
import sys
from gym.envs.toy_text import discrete

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class GridWorld(discrete.DiscreteEnv):
    """
    This is the gridworld environment from Sutton and Barto's book.
    It's described in Chapter 4. The agent is placed on an MXN grid
    and needs to make it to terminal states on the top-left or bottom-right
    to get scored.
    
    The agent cannot go off the edge of the board. And it receives a reward
    of -1 for every state that's not a terminal state. Cruel shit, man.
    """
    metadata = {"render.modes" : ["human"]}
    
    def __init__(self, shape=(5,5)):
        if(not isinstance(shape, (list, tuple))):
            raise ValueError("Unknown type specified for shape: " + \
                             "{}. Should be list/tuple.".format(type(shape)))
        self.shape = shape
        
        #number of states and actions
        nS = numpy.prod(shape)
        nA = 4
        
        #expose transition matrix for dynamic programming
        self.T = self.make_transition_matrix(self.shape)
        
        #uniform state distribution
        dist = numpy.ones(nS) / nS
        
        super(GridWorld, self).__init__(nS, nA, self.T, dist)
        
    def _render(self, mode='human', close=False):
        if(close):
            return
        
        grid = numpy.arange(self.nS).reshape(self.shape)
        iterator = numpy.nditer(grid, flags=['multi_index'])
        while(not iterator.finished):
            s = iterator.iterindex
            y, x = iterator.multi_index
            
            if(self.s == s):
                output = " x "
            elif(s == 0 or s == self.nS - 1):
                output = " T "
            else:
                output = " o "
                
            if(x == 0):
                output = output.lstrip()
            if(x == self.shape[1] - 1):
                output = output.rstrip()
            sys.stdout.write(output)
            
            if(x == self.shape[1] - 1):
                sys.stdout.write("\n")
            
            iterator.iternext()
        sys.stdout.write("\n")
        
        
    @staticmethod
    def make_transition_matrix(shape, n_actions=4):
        """
        Creates a transition probability matrix for gridworld
        
        Inputs
        ------
            @param shape: Tuple specifying the shape of the gridworld environment
            @param n_actions: The number of actions for the environment
        
        Outputs
        -------
            Transition matrix in the format DiscreteEnv requires to work right.
        """
        T = {}
        grid = numpy.zeros(shape=shape)
        iterator = numpy.nditer(grid, flags=['multi_index'])
        nS = numpy.prod(shape)
        
        MAX_Y = shape[0]
        MAX_X = shape[1]
        
        while(not iterator.finished):
            s = iterator.iterindex
            y, x = iterator.multi_index
            
            T[s] = {a : [] for a in range(n_actions)}
            is_terminal = lambda s: s == 0 or s == nS - 1
            reward = 0.0 if is_terminal(s) else -1.0
            
            #if in terminal state
            if(is_terminal(s)):
                T[s][UP] = [(1.0, s, reward, True)]
                T[s][DOWN] = [(1.0, s, reward, True)]
                T[s][LEFT] = [(1.0, s, reward, True)]
                T[s][RIGHT] = [(1.0, s, reward, True)]
            else:
                s_prime_up = s if y == 0 else s - MAX_X
                s_prime_down = s if y == (MAX_Y - 1) else s + MAX_X
                s_prime_left = s if x == 0 else s - 1
                s_prime_right = s if x == (MAX_X - 1) else s + 1
                T[s][UP] = [(1.0, s_prime_up, reward, is_terminal(s_prime_up))]
                T[s][DOWN] = [(1.0, s_prime_down, reward, is_terminal(s_prime_down))]
                T[s][LEFT] = [(1.0, s_prime_left, reward, is_terminal(s_prime_left))]
                T[s][RIGHT] = [(1.0, s_prime_right, reward, is_terminal(s_prime_right))]

            iterator.iternext()
        return T
        
if __name__ == "__main__":
    """
    Test everything works as required
    """
    grid = GridWorld((5, 5))
    grid.reset()
    for i in range(100):
        grid.render()
        action = int(raw_input())
        o, r, done, info = grid.step(action)
        if(done):
            break