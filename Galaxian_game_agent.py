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
    lives = 35
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
        vidas = 3
        killed = 0
        while not done:
            observ = analisis.analisis_imagen(ob)
            frame += 1
            factor = 0.5
        

            #ob = cv2.resize(ob, (inx, iny))
            #ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            #ob = np.reshape(ob, (inx, iny))

            #imgarray = np.ndarray.flatten(ob)

            observ =  observ + [lives]

            nnOutput = net.activate(observ)
            


            numerical_input = nnOutput.index(max(nnOutput))

            ob, reward, done, truncated, info = env.step(numerical_input)

            vidas = info["lives"]

            fitness_current += reward
            if reward > 0:
                counter = 0
                killed +=1
                #enemigos ascecinados
                lives -= 1
            else:
                counter +=1

            if(vidas <=2 ): 
                done = True
            
            if(counter > 6000 ):
                done = True

            

        



        genome.fitness = killed
        
        if done:
            print( i,killed, fitness_current)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'galaxian_config')


def run_neat():
    p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-763")
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 120)

    # save the winner
    with open('winner_more_data1.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)

run_neat()