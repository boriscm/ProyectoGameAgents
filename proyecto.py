import gym
import random
env = gym.make("ALE/Galaxian-v5", render_mode='human')
height, widt, channels = env.observation_space.shape
actions = env.action_space.n

print(env.unwrapped.get_action_meanings())

episodes = 5

data = {}
for episode in range(1,episodes+1):
    state = env.reset()
    done = False
    score = 0
    while not done:
        env.render()
        action = random.choice([0,1,2,3,4,5])
        data = env.step(action)
        n_state = data[0]
        reward = data[1] 
        done_data = (data[2], data[3])
        info = data[4]
        score += reward
        if info["lives"] == 0:
            done = True
    print('Episode: {} score:{}'.format(episode, score))
env.close()
