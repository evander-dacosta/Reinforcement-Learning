#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 11:11:38 2017

@author: evander
"""

import numpy
import sys
if("../") not in sys.path:
    sys.path.append("../")
from envs.gridworld import GridWorld


env = GridWorld((4,4))

def policy_evaluation(policy, env, discount_gamma = 1.0, theta=1e-5):
    """
    Evaluate a given policy given the environment
    
    Inputs
    ------
        @param policy: an S x A matrix representing the probability of taking 
                        an action a given state s
        @param env: OpenAI gym environment
        @param discount_gamma: gamma discount
        @param theta: Tests for convergence of the policy evaluation
    
    Outputs
    -------
        Vector of length env.nS representing the Value function for the input
        policy
    """
    V = numpy.zeros(env.nS)
    while True:
        delta = 0.
        for s in numpy.arange(env.nS):
            v = 0
            for a, a_prob in enumerate(policy[s]):
                for transition_prob, next_state, reward, done in env.T[s][a]:
                    v += a_prob * transition_prob * (reward + (discount_gamma * \
                                                      V[next_state]))
            delta = max(delta, numpy.abs(v - V[s]))
            V[s] = v
        if(delta < theta):
            break
    return V
    
    
if __name__ == "__main__":
    #create a uniform policy
    policy = numpy.ones((env.nS, env.nA)) / env.nA
    v = policy_evaluation(policy, env)
    
    print "Grid's Value function;\n"
    print v.reshape(env.shape)