from controller import Robot
import sys

print("Python Version {}".format(str(sys.version).replace('\n', '')))
# time in [ms] of a simulation step
TIME_STEP = 1600

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()
print(robot.getName())

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)
robot.getDevice("receiver").enable(1)

# feedback loop: step simulation until receiving an exit event
while robot.step(TIME_STEP) != -1:
    
    if robot.getDevice("receiver").getQueueLength() > 0:
        message = robot.getDevice("receiver").getData().decode("utf-8")
        if len(message)>4:
            print(message)
            if robot.getName()=="e-puck1":
                action = message[4]
            else:
                action = message[10]
            print(robot.getName()+":"+action)
            if action=='1':
                leftMotor.setVelocity(6.28)
                rightMotor.setVelocity(6.28)
            elif action=='2':
                leftMotor.setVelocity(-6.28)
                rightMotor.setVelocity(-6.28)
            elif action=='3':
                leftMotor.setVelocity(6.28)
                rightMotor.setVelocity(-6.28)
            elif action=='4':
                leftMotor.setVelocity(-6.28)
                rightMotor.setVelocity(6.28)
            else:
                leftMotor.setVelocity(0)
                rightMotor.setVelocity(0)
        robot.getDevice("receiver").nextPacket()