import ray
from gym.spaces import Box, Discrete
from ray.rllib.agents.trainer_template import build_trainer
from ray.tune import register_env
from ray.tune.logger import pretty_print
from ray.rllib.agents.ppo import PPOTorchPolicy
from ray.rllib.agents.dqn import DQNTorchPolicy
from webots_module.webots_env import WebotsEnv

ray.init()

register_env("Webots-v0", lambda _: WebotsEnv())
obs_space = Box(-16, 16, shape=(6,))
act_space = Discrete(5)

MY_Trainer = build_trainer(
    name="Multi_Agent",
    default_policy=None,
)

config = {
    "multiagent": {
        "policies": {
            "robot1": (PPOTorchPolicy, obs_space, act_space, {}),
            "robot2": (DQNTorchPolicy, obs_space, act_space, {}),
        },
        "policy_mapping_fn":
            lambda agent_id:
            "robot1"
            if agent_id == 0
            else "robot2"
    },
}
trainer = MY_Trainer(env='Webots-v0', config=config)

for i in range(10):
    result = trainer.train()
    print(pretty_print(result))

checkpoint_path = trainer.save()
print(checkpoint_path)
