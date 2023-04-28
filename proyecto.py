
import argparse
import gym
import os
import numpy as np
import random
import neat
from neat import nn, population, statistics, parallel

import datos_y_posiciones as an


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

    informacion =    an.analisis_imagen(state)
    
    
    #mi posicion
    #posicion_nave = ()
    #negro = True
    #pos_x = 0
    #for y in range(len(state[181])):
    #    color = state[181   ][y]
    #    valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
    #    if( valor != "0-0-0"  and valor !="210-164-74"):
    #        if(negro):
    #            pos_x+=y
    #            negro = False
    #    else:
    #        if(not negro):
    #            posicion_nave = (181, int((pos_x+y-1)/2))
     #           pos_x=0
     #           break

#            negro = True
    
    
    
    
    posiciones = {}

    #posicion de cada alien y numero de aliens por fila
    #filas = [23,35,47,59,71,83]
    #filas_aliens = {}
    #negro = True
    #pos_x = 0
    #for y in filas:
    #    filas_aliens[y] = 0
    #    for x in range(len(state[y])):
    #        color = state[y][x]
    #        valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
    #       if( valor != "0-0-0"  and valor !="210-164-74"):
    #            if(negro):
    #                pos_x+=x
    #                filas_aliens[y] +=1
    #                negro = False
    #        else:
    #            if(not negro):
    #                posiciones[len(posiciones)] = (y, int((pos_x+x-1)/2))
    #                pos_x=0

#                negro = True


    #usado para encontrar las posiciones centrales de cada fila de naves y del jugador
    #for x in range(len(state)):
        #for y in range(len(state[x])):
            #color = state[x][y]
            #valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
            #if( valor != "0-0-0"  and valor !="210-164-74"):
                #posiciones[x] = [(x,y), valor]
                #break
                #if(valor not in posiciones):
                    #posiciones[valor] = 1
                #else:
                    #posiciones[valor]+=1

    

                
    #print(len(posiciones))
    #if(len(posiciones) == 37):
    #    a=1

    reward = data[1] 
    done_data = (data[2], data[3])
    info = data[4]
    score += reward
    if info["lives"] == 0:
        done = True



