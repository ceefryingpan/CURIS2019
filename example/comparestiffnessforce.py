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

def get_readings(motors):
    curr1 = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr2 = reader.Read_Value(motors[1], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr3 = reader.Read_Value(motors[2], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr4 = reader.Read_Value(motors[3], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)

    return curr1, curr2, curr3, curr4

def move_arm(curr1, curr2, curr3, curr4):
    while True:
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 + 20)
                curr1 += 20
            if keyboard.is_pressed('a'):
                reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 20)
                curr1 -= 20
            if keyboard.is_pressed('w'):
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 + 20)
                curr2 += 20
            if keyboard.is_pressed('s'):
                reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 - 20)
                curr2 -= 20
            if keyboard.is_pressed('e'):
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3 + 20)
                curr3 += 20
            if keyboard.is_pressed('d'):
                reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3 - 20)
                curr3 -= 20
            if keyboard.is_pressed('r'):
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 + 20)
                curr4 += 20
            if keyboard.is_pressed('f'):
                reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 - 20)
                curr4 -= 20
            if keyboard.is_pressed('z'):
                return
            else:
                pass
        except:
            break

if __name__ == '__main__':

    reader = DynamixelReader()

    motors = [reader.m1id, reader.m2id, reader.m3id, reader.m4id]

    ADDR_PRO_GOAL_POSITION = 116  # address of the goal position and present position
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4  # length of size of goal and present position
    LEN_PRO_PRESENT_POSITION = 4

    N_OBJECTS = 2
    index = -1
    smallestdistance = 1000000

    for i in range(N_OBJECTS):
        curr1, curr2, curr3, curr4 = get_readings(motors)

        print("Move arm to starting position, press z when finished")
        move_arm(curr1, curr2, curr3, curr4)
        curr1, curr2, curr3, curr4 = get_readings(motors)

        print("Ready to read")
        time.sleep(2)

        moving = True
        distance = 0
        while moving:
            # move down until threshold is reached
            reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 + 1)
            curr2 += 1
            reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 - 1)
            curr4 -= 1

            distance += 1

            [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
            if dxl2_current > 150 and distance < smallestdistance:
                index = i + 1
                distance = smallestdistance
                moving = False

    print("The stiffest object is", end=" ")
    print(index)


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