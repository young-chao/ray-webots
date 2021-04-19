import os
from controller import Supervisor

os.environ["WEBOTS_ROBOT_NAME"] = "e-puck0"

# time in [ms] of a simulation step
TIME_STEP = 64
MAX_SPEED = 6.28

# create the Robot instance.
robot = Supervisor()

leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)
emitter = robot.getEmitter("emitter")
robot.getReceiver("receiver").enable(1)

# feedback loop: step simulation until receiving an exit event
while robot.step(TIME_STEP) != -1:
    string_action = "11111111"
    string_action = string_action.encode("utf-8")
    emitter.send(string_action)
    pass
