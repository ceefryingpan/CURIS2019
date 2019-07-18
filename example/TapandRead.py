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

if __name__ == '__main__':

    reader = DynamixelReader()

    fname = "out4_foamtap4.csv"
    fout = open(fname, "w")
    print("Timestamp, Current1, Current2, Current3, Current4", file=fout)

    motors = [reader.m1id, reader.m2id, reader.m3id, reader.m4id]

    ADDR_PRO_GOAL_POSITION = 116  # address of the goal position and present position
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4  # length of size of goal and present position
    LEN_PRO_PRESENT_POSITION = 4

    curr1 = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr2 = reader.Read_Value(motors[1], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr3 = reader.Read_Value(motors[2], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    curr4 = reader.Read_Value(motors[3], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)

    print("Start Reading")
    time.sleep(3)

    # move down first
    N_QUERIES = 50
    timestamp = 0
    for num in range(N_QUERIES):
        reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 + 1)
        curr2 += 1
        reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 - 1)
        curr4 -= 1

        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        # set goal position example
        difft = timestamp - oldtimestamp
        print(
            "%09d,%05d,%05d,%05d,%05d, %d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current, difft))
        print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
              file=fout)

    print("Move down finished")

    # pause and take reading
    time.sleep(0.5)
    [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
    print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
          file=fout)
    time.sleep(0.5)

    # move up
    for num in range(N_QUERIES):
        reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 - 1)
        curr2 -= 1
        reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 + 1)
        curr4 += 1

        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        # set goal position example
        difft = timestamp - oldtimestamp
        print("%09d,%05d,%05d,%05d,%05d, %d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current, difft))
        print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
              file=fout)

    print("Move up finished")

    del reader
    fout.close()
    print("Reading done!")

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