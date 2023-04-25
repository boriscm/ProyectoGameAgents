import gym
import random
import neat
import os
import cv2
import numpy as np

import pickle

import datos_y_posiciones as analisis



env = gym.make("ALE/Galaxian-v5", render_mode='rgb_array')

imgarray=[]

height, widt, channels = env.observation_space.shape
actions = env.action_space.n

def eval_genomes(genomes, config):
    i = 0
    print(len(genomes))
    for genome_id, genome in genomes:
        i+=1

        ob, info = env.reset()

        inx, iny, inc = env.observation_space.shape


        inx= int(inx/8)
        iny = int(iny/8)

        #Extracting basic info that will be used for fitness


        net = neat.nn.RecurrentNetwork.create(genome, config)

        fitness_current = 0

        frame = 0
        counter = 0

        done = False

        while not done:
            observ = analisis.analisis_imagen(ob)
            frame += 1
            factor = 0.5
        

            ob = cv2.resize(ob, (inx, iny))
            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            ob = np.reshape(ob, (inx, iny))

            imgarray = np.ndarray.flatten(ob)


            

            nnOutput = net.activate(observ)
            


            numerical_input = nnOutput.index(max(nnOutput))

            ob, reward, done, truncated, info = env.step(numerical_input)



            fitness_current += reward

            if reward > 0:
                counter = 0
            else:
                counter +=1
            
            if(counter > 6000 ):
                done = True

            

            #evryt time it dies it adss 60 to the score and for me it shouldnt be taken
        

            #este es para eliminar aquellos que mueren al chocar y eliminar a las entidades


        genome.fitness = fitness_current
        
        if done:
            print( i,fitness_current)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'galaxian_config')

p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

winner = p.run(eval_genomes, 100)

# save the winner
with open('winner_try.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)