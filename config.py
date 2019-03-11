"""
CAR CONFIG

This file is read by your car application's manage.py script to change the car
performance.

EXMAPLE
-----------
import dk
cfg = dk.load_config(config_path='~/mycar/config.py')
print(cfg.CAMERA_RESOLUTION)

"""


import os

# PATHS
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(CAR_PATH, 'data')
MODELS_PATH = os.path.join(CAR_PATH, 'models')

# VEHICLE
DRIVE_LOOP_HZ = 20
MAX_LOOPS = 100000

# CAMERA
CAMERA_RESOLUTION = (120, 160) #(height, width)
CAMERA_FRAMERATE = DRIVE_LOOP_HZ


## TA7291P (without Vref)

# LEFT MOTOR
LEFT_MOTOR_IN1_GPIO = 38
LEFT_MOTOR_IN2_GPIO = 40

# RIGHT MOTOR
RIGHT_MOTOR_IN1_GPIO = 35
RIGHT_MOTOR_IN2_GPIO = 37

# TRAINING
BATCH_SIZE = 128
TRAIN_TEST_SPLIT = 0.8

# TUB
TUB_PATH = os.path.join(CAR_PATH, 'tub') # if using a single tub

# ROPE.DONKEYCAR.COM
ROPE_TOKEN="GET A TOKEN AT ROPE.DONKEYCAR.COM"
