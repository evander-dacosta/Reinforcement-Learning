#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 21:33:06 2017

@author: evander
"""

import gym
from gym import spaces
from gym.utils import seeding


def cmp(a, b):
    return int((a > b)) - int((a < b))

deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def draw_card(random):
    return random.choice(deck)
    
def draw_hand(random):
    return [draw_card(random) for _ in range(2)]
            
def usable_ace(hand):
    return 1 in hand and sum(hand) + 10 <= 21
    
def sum_hand(hand):
    if(usable_ace(hand)):
        return sum(hand) + 10
    return sum(hand)
    
def is_bust(hand):
    return sum_hand(hand) > 21
    
def score(hand):
    return 0 if is_bust(hand) else sum_hand(hand)
    
def is_natural(hand):
    return sorted(hand) == [1, 10]
    
class BlackJack(gym.Env):
    """
    Gym environment that simulates games of blackjack
    """
    def __init__(self, natural=False):
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Tuple((spaces.Discrete(32),
                                               spaces.Discrete(11),
                                               spaces.Discrete(2)))
        self._seed()
        
        self.natural = natural
        self._reset()
        self.nA = 2
        
    def _seed(self, seed=None):
        self.random, seed = seeding.np_random(seed)
        return [seed]
    
    def _step(self, action):
        assert self.action_space.contains(action)
        if(action):
            self.player.append(draw_card(self.random))
            if(is_bust(self.player)):
                done = True
                reward = -1
            else:
                done = False
                reward = 0
        else:
            done = True
            while(sum_hand(self.dealer) < 17):
                self.dealer.append(draw_card(self.random))
            reward = cmp(score(self.player), score(self.dealer))
            if(self.natural and is_natural(self.player) and reward == 1):
                reward = 1.5
        return self._get_obs(), reward, done, {}
    
    def _get_obs(self):
        return (sum_hand(self.player), self.dealer[0], usable_ace(self.player))
        
    def _reset(self):
        self.dealer = draw_hand(self.random)
        self.player = draw_hand(self.random)
        while(sum_hand(self.player) < 12):
            self.player.append(draw_card(self.random))
        return self._get_obs()
        
        
if __name__ == "__main__":
    env = BlackJack()
    def print_observation(observation):
        score, dealer_score, usable_ace = observation
        print "Player Score: {} (Usable Ace? {}), Dealer Score: {}".format(
                score, usable_ace, dealer_score)
    
    def strategy(observation):
        score, dealer_scorem, usable_ace = observation
        return 0 if score >= 20 else 1
        
    for i in range(20):
        obs = env.reset()
        for t in range(100):
            print_observation(obs)
            action = strategy(obs)
            print "Taking action {}".format(["Stick", "Hit"][action])
            obs, reward, done, _ = env.step(action)
            if(done):
                print_observation(obs)
                print "Game ended. Reward {}\n".format(float(reward))
                break