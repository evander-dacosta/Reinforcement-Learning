#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:13:21 2017

@author: evander
"""

import numpy
import sys
if("../") not in sys.path:
    sys.path.append("../")
from envs.gridworld import GridWorld
from dynamic_programming import policy_evaluation


env = GridWorld((4,4))


def value_iteration(env, discount_gamma=1., theta=1e-5):
    """
    Implements Policy iteration. Policy evaluation is already implemented
    so no need to reimplement that.
    
    Inputs
    ------
        @param env: OpenAi gym environment
        @param discount_gamma: discount factor
        @param theta: tests convergence of value function
    Returns
    -------
        tuple (policy, value) for the optimal policy and value
        policy is a S x A matrix of action probabilities
        value is a S X 1 array of values for each state
    """
    V = numpy.zeros(env.nS)
    policy = numpy.zeros((env.nS, env.nA))
    
    def lookahead(s, V):
        """
        Single-step lookahead
        """
        new_v = numpy.zeros(env.nA)
        for a in numpy.arange(env.nA):
            for transition_prob, next_state, reward, done in env.T[s][a]:
                new_v[a] = transition_prob * (reward + (discount_gamma * \
                                                        V[next_state]))
        return new_v
        
    while True:
        delta = 0
        for s in numpy.arange(env.nS):
            v = V[s]
            new_v = lookahead(s, V)
            max_action = numpy.argmax(new_v)
            V[s] = new_v[max_action]
            delta = max(delta, numpy.abs(v - V[s]))
        if(delta < theta):
            break
    #Find the optimal policy
    for s in numpy.arange(env.nS):
        A = lookahead(s, V)
        max_action = numpy.argmax(A)
        policy[s, max_action] = 1.0

    return policy, V
    
if __name__ == "__main__":
    policy, v = value_iteration(env)
    print "Policy (0=up, 1=down, 2=left, 3=right"
    print numpy.reshape(numpy.argmax(policy, axis=1), env.shape)
    