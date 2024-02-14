import pypot.dynamixel
import itertools
import time

import motor_controller

robot = motor_controller.MotorController()

robot.set_speed(12,50)
time.sleep(0.3)
robot.motor_stop(12)
