
import argparse
import gym
import os
import numpy as np
from neat import nn, population, statistics, parallel

game = "ALE/Galaxian-v5"

parser = argparse.ArgumentParser(description='OpenAI Gym Solver')
parser.add_argument('--max-steps', dest='max_steps', type=int, default=1000,
                    help='The max number of steps to take per genome (timeout)')
parser.add_argument('--episodes', type=int, default=1,
                    help="The number of times to run a single genome. This takes the fitness score from the worst run")
parser.add_argument('--render', action='store_true')
parser.add_argument('--generations', type=int, default=50,
                    help="The number of generations to evolve the network")
parser.add_argument('--checkpoint', type=str,
                    help="Uses a checkpoint to start the simulation")
parser.add_argument('--num-cores', dest="numCores", type=int, default=4,
                    help="The number cores on your computer for parallel execution")
args = parser.parse_args()


def simulate_species(net, env, episodes=1, steps=5000, render=False):
    fitnesses = []
    for runs in range(episodes):
        inputs = my_env.reset()
        cum_reward = 0.0
        for j in range(steps):
            outputs = net.serial_activate(inputs)
            action = np.argmax(outputs)
            inputs, reward, done, _ = env.step(action)
            if render:
                env.render()
            if done:
                break
            cum_reward += reward

        fitnesses.append(cum_reward)

    fitness = np.array(fitnesses).mean()
    print("Species fitness: %s" % str(fitness))
    return fitness


def worker_evaluate_genome(g):
    net = nn.create_feed_forward_phenotype(g)
    return simulate_species(net, my_env, args.episodes, args.max_steps, render=args.render)




config_file = "galaxian_config.txt"

env = gym.make("ALE/Galaxian-v0", render_mode='human')
height, widt, channels = env.observation_space.shape
actions = env.action_space.n

print(env.unwrapped.get_action_meanings())

episodes = 11

data = {}
def eval_genome(genome, config):

    done = False
    score = 0
    while not done:
        env.render()
        action = random.choice([0,1,2,3,4,5])
        data = env.step(action)
        state = data[0]
        reward = data[1] 
        done_data = (data[2], data[3])
        info = data[4]
        score += reward
        if info["lives"] == 0:
            done = True
    return score
    print('Episode: {} score:{}'.format(episode, score))



# Función para evaluar una población de genomas
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

# Función principal
def run_neat(config_file):
    # Cargar la configuración de NEAT
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Crear la población inicial
    population = neat.Population(config)

    # Añadir un reportero para imprimir estadísticas de la población
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Entrenar la población
    winner = population.run(eval_genomes)

    # Mostrar el mejor genoma
    print('\nMejor genoma:\n{!s}'.format(winner))

    # Mostrar estadísticas finales
    print(stats)

run_neat(config_file)
