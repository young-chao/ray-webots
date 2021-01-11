import ray
from algorithm.train_ppo import PPOTrainer, DEFAULT_CONFIG
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

agent = PPOTrainer(config, 'Webots-v0')

for i in range(200):
    result = agent.train()
    print(pretty_print(result))

checkpoint_path = agent.save()
print(checkpoint_path)
