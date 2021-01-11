import math
import os
import gym
import subprocess
import psutil
import threading
from gym.spaces import Box, Discrete
from controller import Supervisor

webots_list = []
os.environ["WEBOTS_ROBOT_NAME"] = 'e-puck1'
os.environ["WEBOTS_PID"] = '3084'
TIME_STEP = 640
MAX_SPEED = 6.28
area_map = [[0 for col in range(16)] for row in range(16)]


def make_env():
    print("make a webots env.")
    subprocess.run(['webots', '--minimize'])


class WebotsEnv(gym.Env):
    stay = 0
    up = 1
    down = 2
    left = 3
    right = 4

    def __init__(self):
        self.webots_id = 0
        for proc in psutil.process_iter():
            if proc.name() == "webots":
                webots_list.append(proc.pid)
                print("pid-%d,name:%s" % (proc.pid, proc.name()))
        threading.Thread(target=make_env).start()
        for proc in psutil.process_iter():
            if proc.name() == "webots":
                if proc.pid not in webots_list:
                    self.webots_id = proc.pid
                    print("pid-%d,name:%s" % (proc.pid, proc.name()))
        os.environ["WEBOTS_PID"] = str(self.webots_id)
        print(os.environ["WEBOTS_PID"])
        self.robot = Supervisor()
        self.map = area_map
        self.num = 0
        self.leftMotor = self.robot.getMotor('left wheel motor')
        self.rightMotor = self.robot.getMotor('right wheel motor')
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        self.action_space = Discrete(5)
        self.observation_space = Box(-16, 16, shape=(6,))

    def reset(self):
        self.map = area_map
        self.num = 0
        self.robot.getFromDef("robot-1").getField("rotation").setSFRotation([0, 1, 0, 1.57])
        self.robot.getFromDef("robot-1").getField("translation").setSFVec3f([0.0625, 0, 0.0625])
        self.robot.simulationResetPhysics()
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        obs = [4, 0, 0, 0, 0, 0]
        return obs

    def step(self, action):
        self.robot.step(TIME_STEP)
        done = False
        info = {}
        position = self.robot.getFromDef("robot-1").getPosition()
        rotation = self.robot.getFromDef("robot-1").getField('rotation').getSFRotation()[3]
        rotation = int(rotation / 0.39)
        x_position = int(math.floor((position[0] + 1) / 0.125))
        z_position = int(math.floor((position[2] + 1) / 0.125))
        if x_position == 0 and z_position == 0:
            obs = [rotation, -1, self.map[x_position + 1][z_position],
                   -1, self.map[x_position][z_position + 1],
                   self.map[x_position][z_position]]
        elif x_position == 15 and z_position == 0:
            obs = [rotation, self.map[x_position - 1][z_position], -1,
                   -1, self.map[x_position][z_position + 1],
                   self.map[x_position][z_position]]
        elif x_position == 0 and z_position == 15:
            obs = [rotation, -1, self.map[x_position + 1][z_position],
                   self.map[x_position][z_position - 1], -1,
                   self.map[x_position][z_position]]
        elif x_position == 15 and z_position == 15:
            obs = [rotation, self.map[x_position - 1][z_position], -1,
                   self.map[x_position][z_position - 1], -1,
                   self.map[x_position][z_position]]
        elif x_position == 0:
            obs = [rotation, -1, self.map[x_position + 1][z_position],
                   self.map[x_position][z_position - 1], self.map[x_position][z_position + 1],
                   self.map[x_position][z_position]]
        elif x_position == 15:
            obs = [rotation, self.map[x_position - 1][z_position], -1,
                   self.map[x_position][z_position - 1], self.map[x_position][z_position + 1],
                   self.map[x_position][z_position]]
        elif z_position == 0:
            obs = [rotation, self.map[x_position - 1][z_position], self.map[x_position + 1][z_position],
                   -1, self.map[x_position][z_position + 1],
                   self.map[x_position][z_position]]
        elif z_position == 15:
            obs = [rotation, self.map[x_position - 1][z_position], self.map[x_position + 1][z_position],
                   self.map[x_position][z_position - 1], -1,
                   self.map[x_position][z_position]]
        else:
            obs = [rotation, self.map[x_position - 1][z_position], self.map[x_position + 1][z_position],
                   self.map[x_position][z_position - 1], self.map[x_position][z_position + 1],
                   self.map[x_position][z_position]]
        if action == self.stay:
            self.leftMotor.setVelocity(0.0)
            self.rightMotor.setVelocity(0.0)
            reward = -4
        else:
            if self.map[x_position][z_position] == 0:
                reward = 1
                self.map[x_position][z_position] = 1
                self.num = self.num + 1
            else:
                reward = -1
            if self.num > 50:
                done = True
            else:
                if action == self.up:
                    self.leftMotor.setVelocity(1.0 * MAX_SPEED)
                    self.rightMotor.setVelocity(1.0 * MAX_SPEED)
                elif action == self.down:
                    self.leftMotor.setVelocity(-1.0 * MAX_SPEED)
                    self.rightMotor.setVelocity(-1.0 * MAX_SPEED)
                elif action == self.left:
                    self.leftMotor.setVelocity(1.0 * MAX_SPEED)
                    self.rightMotor.setVelocity(-1.0 * MAX_SPEED)
                elif action == self.right:
                    self.leftMotor.setVelocity(-1.0 * MAX_SPEED)
                    self.rightMotor.setVelocity(1.0 * MAX_SPEED)
        return obs, reward, done, info

    def render(self):
        print("Area Map is like this:")
        print(self.map)


if __name__ == '__main__':
    env = WebotsEnv()
    obs0 = env.reset()
    num = 0
    while True:
        env.robot.step(TIME_STEP)
        action0 = env.action_space.sample()
        obs0, reward0, done0, info0 = env.step(action0)
        print('step-', num, ':', reward0, env.map)
        num = num + 1
        if num % 20 == 0:
            observation = env.reset()
    env.close()