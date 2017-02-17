#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 21:33:06 2017

@author: evander
"""

import gym

env = gym.make("CartPole-v0")

n_episodes = 1
n_iters = 100

for episode in range(n_episodes):
    observation = env.reset()
    for i in range(n_iters):
        #env.render()
        action = env.action_space.sample()
        print action
        o, r, d, info = env.step(action)
        if(d):
            print "Episode finished after {} steps".format(i + 1)
            break