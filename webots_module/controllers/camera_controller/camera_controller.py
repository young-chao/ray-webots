from controller import Supervisor

# time in [ms] of a simulation step
TIME_STEP = 64

# create the Robot instance.
robot = Supervisor()

robot.step(1000)
camera = robot.getDevice('camera')
camera.enable(64)
i = camera.saveImage('./cam.jpg',100)
print(i)

while robot.step(TIME_STEP) != -1:
    camera.saveImage('./cam.jpg',100)