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

    # start point
    curr1 = 249
    curr2 = 1181
    curr3 = 339
    curr4 = 2564

    N_QUERIES = 50

    # move to starting position
    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1)
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
    reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)

    time.sleep(3)

    # find object first
    found = False
    reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3 - 600)
    while not found:
        reading = reader.Read_Sync_Once()[3]
        if reading < -20:
            print("Object found!")
            curr3 = reader.Read_Value(motors[2], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
            reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3 + 50)
            curr3 += 50
            found = True

    time.sleep(3)
    print("Ready to interrogate.")
    extrema = 1

    reader.Set_Value(motors[2], ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 25)
    for taps in range(3):
        reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3 - 150)
        time.sleep(0.25)
        for repetitions in range(N_QUERIES):
            [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
            if dxl3_current < extrema:
                extrema = dxl3_current
        curr3 -= 10
        reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
        time.sleep(0.25)

    print("The water is ", end="")
    print(((extrema + 35) * 100) / -75, end="")
    print("% full")
    print(extrema)

    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 - 300)
    time.sleep(3)
    del reader
