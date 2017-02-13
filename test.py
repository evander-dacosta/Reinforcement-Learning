# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:56:14 2017

@author: Evander
"""
import numpy
from environment import Environment

class GridWorld1d(Environment):
    """
    Simulates a 1D gridworld.
    States that are not terminal have -1 score
    States that are terminal have 1 score
    """
    def __init__(self, grid_length):
        """
        Initialise the grid.
        In this object, the grid is represented as an array of scores.
        The state of the environment is the index of the array it's in.
        """
        self.grid_length = grid_length
        
        self.grid = numpy.ones((grid_length,)) * -1.
        self.grid[[0, -1]] = 1.
        
        
        self.actions = {'a':-1, 'd':1}
        self.reset()
        
    def translate_action(self, action):
        """
        Working with a for left and d for right
        """
        return self.actions[action]
        
        
    def action(self, action):
        if(not action in self.actions.keys()):
            raise Exception("Unknown action taken")
        action = self.translate_action(action)
        current_state = self.state
        new_state = self.evolve_state(current_state, action)
        reward = self.get_reward(current_state, action, new_state)
        return reward, new_state
        
        
    def evolve_state(self, state, action):
        if(self.game_ended):
            raise Exception("Action played on an ended game. Reset.")
        new_state = state + action
        self.state = new_state
        if(self.state == 0 or self.state == self.grid.shape[0] - 1):
            #End the game
            self.game_ended = True
        return new_state
        
        
    def get_state(self):
        return self.state
        
    def get_reward(self, current_state, action, next_state):
        return self.grid[self.state]
        
    def reset(self):
        self.state = numpy.random.randint(0, high=self.grid_length)
        self.game_ended = False
        
    def __repr__(self):
        rep = ['_']*self.grid_length
        rep[self.state] = 'X'
        return str(rep)

if __name__ == "__main__":
    g = GridWorld1d(5)
    while(not g.game_ended):
        action = raw_input()
        g.action(action)
        print g