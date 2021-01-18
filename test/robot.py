import os
import sys
from controller import Robot

os.environ["WEBOTS_ROBOT_NAME"] = "e-puck2"
os.environ["WEBOTS_PID"] = sys.argv[1]


class RobotEmitterReceiver:
    def __init__(self):
        # initialize the robot and its receiver and emitter
        self.robot = Robot()
        self.timestep = 640
        self.robot.getEmitter("emitter").setChannel(1)
        self.robot.getReceiver("receiver").setChannel(2)
        self.robot.getReceiver("receiver").enable(1)
        self.leftMotor = self.robot.getMotor('left wheel motor')
        self.rightMotor = self.robot.getMotor('right wheel motor')
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        self.motorSpeeds = [0.0, 0.0]

    def receiveAction(self):
        if self.robot.getReceiver("receiver").getQueueLength() > 0:
            message = self.robot.getReceiver("receiver").getData().decode("utf-8")
            self.doAction(message)
            print(message)
            self.robot.getReceiver("receiver").nextPacket()

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

    def run(self):
        print("ro_run")
        while self.robot.step(self.timestep) != -1:
            print("---------------")
            self.receiveAction()


if __name__ == '__main__':
    print("robot2:"+os.environ["WEBOTS_PID"])
    ro = RobotEmitterReceiver()
    ro.run()
