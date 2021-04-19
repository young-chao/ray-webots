import math
import os
import subprocess
from gym.spaces import Box, Discrete
from controller import Supervisor
from ray.rllib.env.multi_agent_env import MultiAgentEnv

# variables of webots
os.environ["WEBOTS_ROBOT_NAME"] = "robot-0"
area_map = [[0 for col in range(8)] for row in range(8)]


# the robot1's controller and the supervisor
class WebotsEnv(MultiAgentEnv):
    stay = 0
    up = 1
    down = 2
    left = 3
    right = 4

    # initialize the env
    def __init__(self):
        self.agent_1 = 0
        self.agent_2 = 1
        sp = subprocess.Popen(['webots', '--minimize'])
        self.webots_pid = sp.pid
        os.environ["WEBOTS_PID"] = str(self.webots_pid)
        print(os.environ["WEBOTS_PID"])
        self.supervisor = Supervisor()
        self.map = area_map
        self.timestep = 640
        self.max_speed = 6.28
        self.emitter = self.supervisor.getDevice("emitter")
        self.receiver = self.supervisor.getDevice("receiver")
        # set the channel of receiver and emitter
        self.receiver.setChannel(2)
        self.emitter.setChannel(1)
        self.receiver.enable(1)
        self.leftMotor = self.supervisor.getDevice('left wheel motor')
        self.rightMotor = self.supervisor.getDevice('right wheel motor')
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        self.action_space = Discrete(5)
        self.observation_space = Box(-16, 16, shape=(6,))

    # reset the env
    def reset(self):
        self.map = area_map
        self.supervisor.getFromDef("robot-1").getField("rotation").setSFRotation([0, 1, 0, 0])
        self.supervisor.getFromDef("robot-1").getField("translation").setSFVec3f([-0.2, 0, 0])
        self.supervisor.getFromDef("robot-2").getField("rotation").setSFRotation([0, 1, 0, 0])
        self.supervisor.getFromDef("robot-2").getField("translation").setSFVec3f([0.2, 0, 0.1])
        self.supervisor.simulationResetPhysics()
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        self.sendAction(str({0: 0, 1: 0}))
        obs = {
            self.agent_1: [0, 0, 0, 0, 0, 0],
            self.agent_2: [0, 0, 0, 0, 0, 0]
        }
        return obs

    # step the action(for both robot1 and robot2)
    def step(self, action):
        self.supervisor.step(self.timestep)
        self.sendAction(str(action))
        position1 = self.supervisor.getFromDef("robot-1").getPosition()
        position2 = self.supervisor.getFromDef("robot-2").getPosition()
        rotation1 = self.supervisor.getFromDef("robot-1").getField("rotation").getSFRotation()[3]
        rotation2 = self.supervisor.getFromDef("robot-2").getField("rotation").getSFRotation()[3]
        # rotation1 = int(rotation1 / 0.39)
        # rotation2 = int(rotation2 / 0.39)
        x1_position = int(math.floor((position1[0] + 0.5) / 0.125))
        z1_position = int(math.floor((position1[2] + 0.5) / 0.125))
        x2_position = int(math.floor((position2[0] + 0.5) / 0.125))
        z2_position = int(math.floor((position2[2] + 0.5) / 0.125))
        obs = {
            self.agent_1: [rotation1, rotation2, x1_position, z1_position, x2_position, z2_position],
            self.agent_2: [rotation2, rotation1, x2_position, z2_position, x1_position, z1_position]
        }
        reward = {
            self.agent_1: 0,
            self.agent_2: 1
        }
        if math.pow((x1_position - x2_position), 2) + math.pow((z1_position - z2_position), 2) < 0.2:
            reward[self.agent_1] = 0.1
        elif math.pow((x1_position - x2_position), 2) + math.pow((z1_position - z2_position), 2) < 0.05:
            reward[self.agent_1] = 1
        done = {
            '__all__': False,
            self.agent_1: False,
            self.agent_2: False
        }
        info = {}
        return obs, reward, done, info

    # render the env's map
    def render(self):
        print("Area Map is like this:")
        print(self.map)

    # send the action to the robot2
    def sendAction(self, action):
        print('send the action to the robot.')
        string_action = action
        string_action = string_action.encode("utf-8")
        self.emitter.send(string_action)


# test the env
if __name__ == '__main__':
    env = WebotsEnv()
    obs0 = env.reset()
    num = 0
    while True:
        # env.supervisor.step(env.timestep)
        action0 = env.action_space.sample()
        action1 = env.action_space.sample()
        obs0, reward0, done0, info0 = env.step({0: action0, 1: action1})
        print('step-', num, ':', reward0)
        num = num + 1
        if num % 200 == 0:
            observation = env.reset()
    env.close()
