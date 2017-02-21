#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:38:04 2017

@author: evander
"""

import numpy
import gym
import sys
from gym.envs.toy_text import discrete

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class WindyGridWorld(discrete.DiscreteEnv):
    metadata = {'render.modes':['human']}
    
    def _limit_coords(self, coord):
        """
        Limit the coordinates of the agent to within the map
        """
        coord[0] = min(coord[0], self.shape[0] - 1)
        coord[0] = max(coord[0], 0)
        coord[1] = min(coord[1], self.shape[1] - 1)
        coord[1] = max(coord[1], 0)
        return coord
        
    def _transition_prob(self, current, delta, winds):
        """
        Calculate transition probability given winds
        """
        new_position = numpy.array(current) + numpy.array(delta) + \
                       numpy.array([-1, 0]) * winds[tuple(current)]
        new_position = self._limit_coords(new_position).astype(int)
        new_state = numpy.ravel_multi_index(tuple(new_position), self.shape)
        is_done = tuple(new_position) == (3, 7)
        return [(1.0, new_state, -1.0, is_done)]
    
    def __init__(self):
        self.shape = (7, 10)
        nS = numpy.prod(self.shape)
        nA = 4
        
        #Winds
        winds = numpy.zeros(self.shape)
        winds[:, [3,4,5,8]] = 1
        winds[:, [6,7]] = 2
        
        #Transition matrix
        P = {}
        for s in range(nS):
            position = numpy.unravel_index(s, self.shape)
            P[s] = {a : [] for a in range(nA)}
            P[s][UP] = self._transition_prob(position, [-1, 0], winds)
            P[s][DOWN] = self._transition_prob(position, [1, 0], winds)
            P[s][LEFT] = self._transition_prob(position, [0, -1], winds)
            P[s][RIGHT] = self._transition_prob(position, [0, 1], winds)
            
        #we always start in (3, 0)
        isd = numpy.zeros(nS)
        isd[numpy.ravel_multi_index((3, 0), self.shape)] = 1.0
            
        super(WindyGridWorld, self).__init__( nS, nA, P, isd)
        
    def _render(self, mode='human', close=False):
        if(close):
            return
        for s in range(self.nS):
            position = numpy.unravel_index(s, self.shape)
            if(self.s == s):
                output = ' x '
            elif(position == (3, 7)):
                output = ' T '
            else:
                output = ' o '
            if(position[1] == 0):
                output = output.lstrip()
            if(position[1] == self.shape[1] - 1):
                output = output.rstrip()
                output += "\n"
            sys.stdout.write(output)
        sys.stdout.write('\n')

if __name__ == "__main__":
    """
    Test everything works as required
    """
    grid = WindyGridWorld()
    grid.reset()
    for i in range(100):
        grid.render()
        action = int(raw_input())
        o, r, done, info = grid.step(action)
        if(done):
            break        