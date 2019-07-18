#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 12:50:09 2019

@author: Charles Pan, Ante Qu

Testing interrupt of arm.

"""

from CurrentReader import *
import numpy as np
# from scipy.signal import butter, lfilter, freqz
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
        reader.Set_Value(motor, ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 75)

    # set profile acceleration
    ADDR_PRO_ACCEL = 108
    LEN_PRO_ACCEL = 4
    for motor in motors:
        reader.Set_Value(motor, ADDR_PRO_ACCEL, LEN_PRO_ACCEL, 10000)

    print("Moving to starting position!")

    # move to starting position
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1195)
    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 805)
    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 308)
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2919)

    time.sleep(5)

    # move to next position
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, -725)
    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 843)
    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 308)
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2919)

    time.sleep(0.5)

    # move back to starting position to test interrupt
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 1195)
    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 805)
    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 308)
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2919)

    time.sleep(3)

    print("Testing done")
