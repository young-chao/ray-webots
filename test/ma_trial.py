import gym
import ray
from gym.spaces import Box, Discrete
from ray.rllib.agents.trainer_template import build_trainer
from ray.tune import register_env
from ray.tune.logger import pretty_print
from ray.rllib.agents.ppo import PPOTFPolicy, PPOTorchPolicy, PPOTrainer
from ray.rllib.agents.dqn import DQNTFPolicy, DQNTorchPolicy
from env.webots_env import WebotsEnv

ray.init()

register_env("Webots-v0", lambda _: WebotsEnv())
obs_space = Box(-16, 16, shape=(5,))
act_space = Discrete(5)

agent = PPOTrainer(
    env='Webots-v0',
    config={
        "multiagent": {
            "policies": {
                "robot1": (None, obs_space, act_space, {}),
                "robot2": (None, obs_space, act_space, {}),
            },
            "policy_mapping_fn":
                lambda agent_id:
                    "robot1"
                    if agent_id == 0
                    else "robot2"
        },
    }
)

for i in range(10):
    result = agent.train()
    print(pretty_print(result))
