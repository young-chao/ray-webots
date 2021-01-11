import time
import ray
import gym
from algorithm.test_ppo import PPOTrainer, DEFAULT_CONFIG
from ray.tune.logger import pretty_print

ray.init()

config = DEFAULT_CONFIG.copy()
config['num_workers'] = 1
config['num_cpus_per_worker'] = 1
config['num_sgd_iter'] = 20
config['rollout_fragment_length'] = 20
config['train_batch_size'] = 4000
config['sgd_minibatch_size'] = 200
config['model']['fcnet_hiddens'] = [100, 100]

print('env-make')
env = gym.make("Webots-v1")
state = env.reset()
done = False
cumulative_reward = 0

print('agent')
# time.sleep(5)
test_agent = PPOTrainer(config, 'Webots-v0')
print('restore')
test_agent.restore('/home/zhaoyong/ray_results/PPO_Webots-v3_2021-01-04_15-22-19vjr5lnpi/checkpoint_10/checkpoint-10')

# time.sleep(10)

while not done:
    action = test_agent.compute_action(state)
    state, reward, done, _ = env.step(action)
    cumulative_reward += reward
    print(cumulative_reward)

print('last:', cumulative_reward)