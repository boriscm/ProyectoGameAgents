import gym
import random
import neat
import os
import cv2
import numpy as np

import pickle


env = gym.make("ALE/Galaxian-v5", render_mode='human')

imgarray=[]

height, widt, channels = env.observation_space.shape
actions = env.action_space.n

def eval_genomes(genomes, config):
    i = 0
    for genome_id, genome in genomes:
        i+=1

        ob, info = env.reset()

        inx, iny, inc = env.observation_space.shape


        inx= int(inx/8)
        iny = int(iny/8)

        net = neat.nn.RecurrentNetwork.create(genome, config)

        fitness_current = 0

        frame = 0
        counter = 0

        done = False

        while not done:
            frame += 1
            factor = 0.5

            ob = cv2.resize(ob, (inx, iny))
            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            ob = np.reshape(ob, (inx, iny))

            imgarray = np.ndarray.flatten(ob)

            nnOutput = net.activate(imgarray)


            numerical_input = nnOutput.index(max(nnOutput))

            ob, reward, done, truncated, info = env.step(numerical_input)



            fitness_current += reward

            if reward > 0:
                counter = 0
            else:
                counter +=1

            #evryt time it dies it adss 60 to the score and for me it shouldnt be taken
            if done:
                print( i,fitness_current)

            

            genome.fitness = fitness_current

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'galaxian_config')

p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

winner = p.run(eval_genomes)

# save the winner
with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)