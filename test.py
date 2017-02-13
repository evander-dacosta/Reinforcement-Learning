# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:56:14 2017

@author: Evander
"""
import numpy
import numpy.random
from environment import Environment


class GridWorldAgent(object):
    """
    The GridWorldAgent has it's own internal representation 
    of:
    Policy function p(action|state)
    Value function V(state)
    
    Methods
    -------
    get_action(state): Gets the action according to current policy
    get_value(state): Gets the value according to current state
    initialise_policy(): Initialises the agent's action policy
    initialise_values(): Initialises the agent's value function
    evaluate_policy(num_iters): Evaluates the agent's policy and updates the internal
                        representation of environment's value
    update_policy(): Update's the agent's policy based on greedy methods
    iteration_step(): A single iteration step on the Value Iteration method
    """
    
    def __init__(self, grid_world, gamma=0.4):
        self.grid_world = grid_world
        self.gamma = gamma
        self.policy = self.initialise_policy()
        self.values = self.initialise_values()
        
        
    def initialise_policy(self):
        """
        Initialise by making agent go right all the time
        """
        policy = numpy.zeros(shape=(self.grid_world.grid_length, 2))
        policy[1:-1, :] = 0.5
        return policy
        
    def initialise_values(self):
        """
        Initialise with zero values for all states
        """
        return numpy.zeros((self.grid_world.grid_length,))
        
    def get_action(self, state):
        if(state == 0 or state ==self.grid_world.grid.shape[0] - 1):
            return 't'
        choices = self.policy[state]
        action = numpy.random.choice(['a', 'd'], 1, p=choices)
        return action[0]
        
    
    def evaluate_policy(self, num_iters=1):
        for iter in range(num_iters):
            for s in range(len(self.grid_world.grid)):
                a = self.get_action(s)
                s_prime = self.grid_world.evolve_state(s, a)
                reward = self.grid_world.get_reward(s, a, s_prime)
                if(s_prime is None):
                    future_reward = 0
                else:
                    future_reward = self.values[s_prime]
                self.values[s] = reward + (self.gamma * future_reward )
    
    def update_policy(self):
        pass
    
    def iteration_step(self):
        pass


if __name__ == "__main__":
    from gridworld import GridWorld1d
    g = GridWorld1d(7)
    agent = GridWorldAgent(g)
    agent.evaluate_policy(100)
    print agent.values
    