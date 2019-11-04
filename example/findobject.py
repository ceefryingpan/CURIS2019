#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 12:50:09 2019

@author: Charles Pan, Jason Ah Chuen, Ante Qu

Arm keeps moving in the specified direction until an obstacle (constant event) is hit.
Prints position of obstacle

"""

from CurrentReader import *
import time

if __name__ == '__main__':

    reader = DynamixelReader()

    ADDR_PRO_GOAL_POSITION = 116
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4
    LEN_PRO_PRESENT_POSITION = 4
    motors = [reader.m1id, reader.m2id, reader.m3id, reader.m4id]

    N_QUERIES = 10000000

    # set profile velocity
    ADDR_PRO_VELOCITY = 112
    LEN_PRO_VELOCITY = 4
    for motor in motors:
        reader.Set_Value(motor, ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 25)

    # set profile acceleration
    ADDR_PRO_ACCEL = 108
    LEN_PRO_ACCEL = 4
    for motor in motors:
        reader.Set_Value(motor, ADDR_PRO_ACCEL, LEN_PRO_ACCEL, 100)

    print("Moving to starting position!")

    curr1 = 206
    curr2 = 1081 - 200
    curr3 = 329
    curr4 = 2639

    # move to starting position
    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1)
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
    reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)
    time.sleep(3)

    print("Ready to move.")

    # TODO: implement some searching motion
    for iterations in range(10):
        reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 676)
        time.sleep(3)
        reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 + 676)
        time.sleep(6)
        reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 + 100)
        reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 - 100)
        curr2 += 100
        time.sleep(1)
    time.sleep(0.5)

    movingavg_dxl1 = 0
    movingavg_dxl2 = 0
    movingavg_dxl3 = 0
    movingavg_dxl4 = 0
    alpha = 0.2
    threshold = 0.2

    while True:  # use a moving average and detect spike if over 20% threshold
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
        if (dxl1_current - movingavg_dxl1) / movingavg_dxl1 > threshold:
            print("Object or event occurred in joint 1")
        if (dxl2_current - movingavg_dxl2) / movingavg_dxl2 > threshold:
            print("Object or event occurred in joint 1")
        if (dxl3_current - movingavg_dxl3) / movingavg_dxl3 > threshold:
            print("Object or event occurred in joint 1")
        if (dxl4_current - movingavg_dxl4) / movingavg_dxl4 > threshold:
            print("Object or event occurred in joint 1")

        # if dxl1_current < -15:
        #     curr1 = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
        #     # curr2 = reader.Read_Value(motors[1], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
        #     # curr3 = reader.Read_Value(motors[2], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
        #     # curr4 = reader.Read_Value(motors[3], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
        #
        #     reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 1)
        #     # reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
        #     # reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
        #     # reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)
        #
        #     print("Object or event detected")
        #     print(curr1, end=" ")
        #     print(curr2, end=" ")
        #     print(curr3, end=" ")
        #     print(curr4)
        #
        #     time.sleep(1)
        #     break

        movingavg_dxl1 = ((1-alpha) * movingavg_dxl1) + (alpha * dxl1_current)
        movingavg_dxl2 = ((1-alpha) * movingavg_dxl2) + (alpha * dxl2_current)
        movingavg_dxl3 = ((1-alpha) * movingavg_dxl3) + (alpha * dxl3_current)
        movingavg_dxl4 = ((1-alpha) * movingavg_dxl4) + (alpha * dxl4_current)

    del reader
