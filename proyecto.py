
import argparse
import gym
import os
import numpy as np
import random
import neat
from neat import nn, population, statistics, parallel

game = "ALE/Galaxian-v5"






config_file = "galaxian_config.txt"

env = gym.make("ALE/Galaxian-v5", render_mode='human')
height, widt, channels = env.observation_space.shape
actions = env.action_space.n

print(env.unwrapped.get_action_meanings())

episodes = 11

data = {}

done = False
score = 0
env.reset()
while not done:
    env.render()
    action = random.choice([0,1,2,3,4,5])
    data = env.step(action)
    state = data[0]
    reward = data[1] 
    done_data = (data[2], data[3])
    info = data[4]
    print(done_data)
    score += reward
    if info["lives"] == 0:
        done = True



