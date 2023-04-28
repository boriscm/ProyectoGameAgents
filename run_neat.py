import gym
import numpy as np
import cv2
import time
import neat

import datos_y_posiciones as analisis


import pickle

env = gym.make("ALE/Galaxian-v5", render_mode='human')


ob, info = env.reset()

config = neat.Config(neat.DefaultGenome,neat.DefaultReproduction,
                    neat.DefaultSpeciesSet,neat.DefaultStagnation,'./config/winer_2nd_model')

with open("winner_2nd_model.pkl", "rb") as f:
    best_bot = pickle.load(f)
net = neat.nn.feed_forward.FeedForwardNetwork.create(best_bot,config)

inx, iny, inc = env.observation_space.shape


inx= int(inx/8)
iny = int(iny/8)

frame = 0
while True:

    observ = analisis.analisis_imagen(ob)


    frame += 1
    env.render()
    ob = cv2.resize(ob, (inx, iny))
    ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
    ob = np.reshape(ob, (inx, iny))


    imgarray = np.ndarray.flatten(ob)
    ai_decision  = net.activate(observ)
    action = np.argmax(ai_decision)
    ob, reward, done, truncated, info = env.step(action)
    if done:
        break

env.close()