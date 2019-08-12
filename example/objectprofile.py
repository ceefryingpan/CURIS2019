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
    ADDR_MOVING = 122
    LEN_MOVING = 1
    motors = [reader.m1id, reader.m2id, reader.m3id, reader.m4id]

    # N_QUERIES = 10000000

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

    # # detection and tipping over start point
    # curr1 = 110
    # curr2 = 1000
    # curr3 = 303
    # curr4 = 2600

    # # sliding start point
    # curr1 = 215
    # curr2 = 1400
    # curr3 = 284
    # curr4 = 2324

    # sliding inverted start point
    curr1 = 301
    curr2 = 1500
    curr3 = -135
    curr4 = 2468

    # move to starting position
    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1)
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
    reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)

    time.sleep(3)
    print("Ready to interrogate.")

    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 600)
    time.sleep(0.25)

    while True:
        dxl1_current = reader.Read_Sync_Once()[1]
        if dxl1_current <= -20:
            print("Object found!")
            found = True
            break

    moving = False
    static = False
    lastreading = 0
    secondtolast = 0

    N_QUERIES = 150

    for queries in range(N_QUERIES):
        dxl1_current = reader.Read_Sync_Once()[1]
        print(dxl1_current)
        if dxl1_current < -250:
            print("Object is immovable!")
            break
        elif dxl1_current > -10:
            print("Object has tipped over or is out of position!")
            break
        elif -75 > dxl1_current > lastreading > secondtolast:
            print("Object is undergoing static friction!")
        elif dxl1_current < lastreading < secondtolast and dxl1_current < -75:
            print("Object is moving!")

        secondtolast = lastreading
        lastreading = dxl1_current

    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 - 600)
    time.sleep(3)

    del reader
