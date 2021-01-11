import ray
import time
from ray.rllib.agents.ppo import PPOTrainer, DEFAULT_CONFIG
from ray.tune.logger import pretty_print

ray.init()


config = DEFAULT_CONFIG.copy()
config['num_workers'] = 2
config['model']['fcnet_hiddens'] = [256, 256]
config['num_cpus_per_worker'] = 1

agent = PPOTrainer(config, 'Webots-v0')

time_1 = time.time()
for i in range(10):
    result = agent.train()
    print(pretty_print(result))

time_2 = time.time()
print('train totally cost', time_2-time_1)

checkpoint_path = agent.save()
print(checkpoint_path)
