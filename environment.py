# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:56:14 2017

@author: Evander
"""

class Environment(object):
    """
    Abstract class which represents the 'Environment' which a 
    Reinforcement Learning agent interacts with
    
    Methods
    -------
    translate_action(): Translates from agent's language of actions to 
                        environment's language of actions
    action(action): Take a certain action
    get_state(): Returns the current state of the environment
    evolve_state(current_state, action): Evolves the current state of the
                                         environment
    get_reward(state, action, next_state): Returns the reward for a given state,
                                           action and next_state
    reset(): Resets the environment
    """
    
    def translate_action(self, action):
        """
        Provides an interface between agent's actions and the 
        environment's implementation of those actions
        
        Inputs
        ------
        @param action: High-level description of action e.g. 'go left'
        
        Returns
        -------
        action: low-level implementation of action e.g. -1
        """
        raise NotImplementedError()
    
    def action(self, action):
        """
        Take an action
        
        Inputs
        ------
        @param action: The action to be taken
        
        Returns
        -------
        reward, new_state
        """
        raise NotImplementedError()
    
    def evolve_state(self, current_state, action):
        """
        Evolve the internal state of the environment
        
        Inputs
        ------
        @param current_state: Current state of the Environment
        @param action: The action taken
        """
        raise NotImplementedError()
        
    def get_state(self):
        """
        Return the internal state of the environment
        
        Returns
        -------
        s: The internal state of the environment
        """
        raise NotImplementedError()
    
    def get_reward(self, state, action, next_state):
        """
        Gets the reward for taking a specific action in a given state.
        
        Inputs
        ------
        @param state: The state the agent was in
        @param action: The action taken
        @param next_state: The subsequent state of the environment, after
                            evolving.
        """
        raise NotImplementedError()
    
    def reset(self, *args, **kwargs):
        """
        Reset the environment
        """
        raise NotImplementedError()
        