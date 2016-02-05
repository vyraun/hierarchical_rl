
import datetime
import numpy as np
import os
import pickle
import sys

LOGGING_DIRECTORY = '../logs'
MAXIMUM_WEIGHT_MAGNITUDE = 1000

class Logger(object):
    """
    :description: tracks and logs information about an agent
    """
    
    def __init__(self, agent_name, logging=True):
        self.agent_name = agent_name
        self.actions = []
        self.rewards = []
        self.losses = []
        self.states = []
        self.weights = None
        self.log_dir = None
        self.logging = logging

    def log_action(self, action):
        self.actions.append(action)

    def log_reward(self, reward):
        self.rewards.append(reward)

    def log_loss(self, loss):
        self.losses.append(loss)

    def log_weights(self, weights):
        self.weights = weights
        max_magnitude = np.max(np.abs(weights.values()))

        if max_magnitude > MAXIMUM_WEIGHT_MAGNITUDE:
            except_string = 'Agent weights have surpassed reasonable values. Max weight: {}'.format(max_magnitude)
            raise ValueError(except_string)

    def log_epoch(self, epoch):
        if not self.logging:
            return

        if self.log_dir is None:
            self.create_log_dir()

        self.record_stat('actions', self.actions, epoch)
        self.record_stat('rewards', self.rewards, epoch)
        self.record_stat('losses', self.losses, epoch)
        self.record_weights(self.weights, epoch)

    def record_stat(self, name, values, epoch):
        filename = '{}_epoch_{}'.format(name, epoch)
        filepath = os.path.join(self.log_dir, filename)
        np.savez(filepath, values=values)

    def record_weights(self, weights, epoch):
        filename = 'weights_epoch_{}.pkl'.format(epoch)
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(weights, f, pickle.HIGHEST_PROTOCOL)

    def create_log_dir(self):
        # would be nice to include 'validation' accuracy in the name
        dir_name = '{}_{}'.format(self.agent_name, datetime.datetime.now().isoformat())
        dir_path = os.path.join(LOGGING_DIRECTORY, dir_name)
        os.mkdir(dir_path)
        self.log_dir = dir_path