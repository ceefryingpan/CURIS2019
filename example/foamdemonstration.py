#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ante Qu, Charles Pan, Jason Ah Chuen

#
# *********     Dynamixel Arm Movement and Current Readings      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using two Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(support.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#
# When running the code in Terminal, the keyboard library requires to run as an administrator.
# Run the code as 'sudo python MoveButtons.py'
# Use q, a, w, s, e, d, r, f to move motors 1, 2, 3, and 4 respectively.
# Use z to quit out of program.

import time
from CurrentReader import *
import keyboard

motors = []

def get_readings():
    curr1 = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr2 = reader.Read_Value(motors[1], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr3 = reader.Read_Value(motors[2], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr4 = reader.Read_Value(motors[3], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)

    return curr1, curr2, curr3, curr4

def tap_object(reader):
    curr1, curr2, curr3, curr4 = get_readings()

    # slower velocity
    for motor in motors:
        reader.Set_Value(motor, ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 10)

    # set trajectory further down
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 + 100)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 - 100)

    while True:
        dxl2_current = reader.Read_Sync_Once()[2]
        if dxl2_current > 250:
            newcurr2 = get_readings()[1]
            reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
            reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)
            return newcurr2


def detect_object(reader):
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1446)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2331)
    time.sleep(1)

    while True:
        dxl2_current = reader.Read_Sync_Once()[2]
        if dxl2_current >= 0:
            print("Object detected")
            curr1, curr2, curr3, curr4 = get_readings()
            reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
            reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)
            return


if __name__ == '__main__':

    reader = DynamixelReader()

    motors = [reader.m1id, reader.m2id, reader.m3id, reader.m4id]
    startingpos = [-300, 901, 311, 2775]

    ADDR_PRO_GOAL_POSITION = 116  # address of the goal position and present position
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4  # length of size of goal and present position
    LEN_PRO_PRESENT_POSITION = 4
    ADDR_PRO_VELOCITY = 112
    LEN_PRO_VELOCITY = 4
    ADDR_PRO_ACCEL = 108
    LEN_PRO_ACCEL = 4
    ADDR_MOVING = 122
    LEN_MOVING = 1

    # set profile acceleration

    for motor in motors:
        reader.Set_Value(motor, ADDR_PRO_ACCEL, LEN_PRO_ACCEL, 100)

    N_OBJECTS = 4
    index = -1
    smallest = 100000000

    for i in range(N_OBJECTS):
        # move to starting position
        print("Moving to starting position")
        for motorindex in range(len(motors)):
            reader.Set_Value(motors[motorindex], ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 50)
            reader.Set_Value(motors[motorindex], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, startingpos[motorindex])
        time.sleep(2)

        # detect object
        print("Searching for object")
        detect_object(reader)
        curr1, curr2, curr3, curr4 = get_readings()

        # tap object
        print("Object found, ready to tap")
        distance = tap_object(reader)
        if distance < smallest:
            index = i
            smallest = distance
        print("Tapping finished")
        time.sleep(0.5)

        # change to next position
        startingpos[0] += 400

    for times in range(N_OBJECTS):
        startingpos[0] -= 400
    startingpos[0] += (index * 400)

    # go to stiffest foam block
    for num in range(len(motors)):
        reader.Set_Value(motors[num], ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 50)
        reader.Set_Value(motors[num], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, startingpos[num])
    time.sleep(1)
    detect_object(reader)
    print("This is the stiffest object")

    time.sleep(5)
    del reader

# miscellaneous
# Control table address
ADDR_PRO_TORQUE_ENABLE = 64  # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION = 116
ADDR_PRO_REALTIME_TICK = 120
ADDR_PRO_PRESENT_POSITION = 132
ADDR_PRO_LED_RED = 65
ADDR_PRO_CURRENT = 126

# Data Byte Length
LEN_PRO_GOAL_POSITION = 4
LEN_PRO_PRESENT_POSITION = 4
LEN_PRO_REALTIME_TICK = 2
LEN_PRO_LED_RED = 1
LEN_PRO_CURRENT = 2

# Protocol version
PROTOCOL_VERSION = 2  # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID = 100  # Dynamixel ID: 1
DXL2_ID = 101  # Dynamixel ID: 2
DXL3_ID = 102  # Dynamixel ID: 3
DXL4_ID = 103  # Dynamixel ID: 4
BAUDRATE = 1000000
DEVICENAME = "COM5".encode('utf-8')  # Check which port is being used on your controller