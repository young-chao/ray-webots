import os
import subprocess
import math
import gym
from gym.spaces import Box, Discrete
from controller import Supervisor
from ray.rllib.env.multi_agent_env import MultiAgentEnv

# variables of webots
os.environ["WEBOTS_ROBOT_NAME"] = "e-puck1"
area_map = [[0 for col in range(16)] for row in range(16)]


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
        subprocess.Popen(['python', 'robot.py', str(self.webots_pid)])
        self.supervisor = Supervisor()
        self.map = area_map
        self.timestep = 640
        self.max_speed = 6.28
        self.emitter = self.supervisor.getEmitter("emitter")
        self.receiver = self.supervisor.getReceiver("receiver")
        # set the channel of receiver and emitter
        self.receiver.setChannel(1)
        self.emitter.setChannel(2)
        self.receiver.enable(1)
        self.leftMotor = self.supervisor.getMotor('left wheel motor')
        self.rightMotor = self.supervisor.getMotor('right wheel motor')
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        self.action_space = Discrete(5)
        self.observation_space = Box(-16, 16, shape=(5,))

    # reset the env
    def reset(self):
        self.map = area_map
        self.supervisor.getFromDef("robot-1").getField("rotation").setSFRotation([0, 1, 0, 1.57])
        self.supervisor.getFromDef("robot-1").getField("translation").setSFVec3f([0.0625, 0, 0.0625])
        self.supervisor.getFromDef("robot-2").getField("rotation").setSFRotation([0, 1, 0, 1.57])
        self.supervisor.getFromDef("robot-2").getField("translation").setSFVec3f([0.5625, 0, 0.0625])
        self.supervisor.simulationResetPhysics()
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        self.sendAction("0")
        obs = {
            self.agent_1: [0, 0, 0, 0, 0],
            self.agent_2: [0, 0, 0, 0, 0]
        }
        return obs

    # step the action(for both robot1 and robot2)
    def step(self, action):
        self.supervisor.step(self.timestep)
        self.sendAction(str(action[self.agent_2]))
        self.doAction(str(action[self.agent_1]))
        obs = {
            self.agent_1: [0, 0, 0, 0, 0],
            self.agent_2: [0, 0, 0, 0, 0]
        }
        reward = {
            self.agent_1: 1,
            self.agent_2: 1
        }
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

    # do the action
    def doAction(self, action):
        if action == "1":
            self.leftMotor.setVelocity(6.28)
            self.rightMotor.setVelocity(6.28)
        elif action == "2":
            self.leftMotor.setVelocity(-6.28)
            self.rightMotor.setVelocity(-6.28)
        elif action == "3":
            self.leftMotor.setVelocity(6.28)
            self.rightMotor.setVelocity(-6.28)
        elif action == "4":
            self.leftMotor.setVelocity(-6.28)
            self.rightMotor.setVelocity(6.28)
        else:
            self.leftMotor.setVelocity(0)
            self.rightMotor.setVelocity(0)


# test the env
if __name__ == '__main__':
    env = WebotsEnv()
    obs0 = env.reset()
    num = 0
    while True:
        # env.supervisor.step(env.timestep)
        action0 = env.action_space.sample()
        obs0, reward0, done0, info0 = env.step(action0)
        print('step-', num, ':', reward0)
        num = num + 1
        if num % 20 == 0:
            observation = env.reset()
    env.close()
