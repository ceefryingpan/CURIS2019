#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 12:50:09 2019

@author: Charles Pan, Jason Ah Chuen, Ante Qu

Live demonstration for CURIS poster session.

"""

from CurrentReader import *
import time

def Check_Horizontal(curr1):
    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 1000)
    time.sleep(0.1)
    for queries1 in range(300):
        dxl1_current = reader.Read_Sync_Once()[1]
        print(dxl1_current)
        if dxl1_current < -30:
            newcurr = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
            reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr + 1)
            print("Object detected")
            time.sleep(1)
            return True

    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 + 1000)
    time.sleep(0.1)
    for queries2 in range(600):
        dxl1_current = reader.Read_Sync_Once()[1]
        print(dxl1_current)
        if dxl1_current > 30:
            newcurr = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
            reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr - 1)
            print("Object detected")
            time.sleep(1)
            return True

    return False

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

if __name__ == '__main__':

    reader = DynamixelReader()

    ADDR_PRO_GOAL_POSITION = 116
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4
    LEN_PRO_PRESENT_POSITION = 4
    ADDR_MOVING = 122
    LEN_MOVING = 1
    motors = [reader.m1id, reader.m2id, reader.m3id, reader.m4id]

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

    # start at high position
    print("Moving to starting position!")

    curr1 = 271
    curr2 = 780
    curr3 = 309
    curr4 = 2914

    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1)
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
    reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)
    time.sleep(3)

    # check horizontally for object
    found = Check_Horizontal(curr1)

    # move to water bottle position
    # start point
    curr1 = 271
    curr2 = 1181
    curr3 = 309
    curr4 = 2564

    # move to starting position
    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1)
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
    reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)
    time.sleep(3)

    # check horizontally for water bottle
    found = Check_Horizontal(curr1)

    # side tap water bottle
    if found:
        newcurr3 = curr3
        reader.Set_Value(motors[2], ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 25)
        for taps in range(3):
            minreading = 1
            reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr3 - 150)
            # time.sleep(0.25)
            for repetitions in range(50):
                [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
                if dxl3_current < minreading:
                    minreading = dxl3_current
            newcurr3 -= 25
            reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr3)
            time.sleep(0.25)

    # print amount of water inside bottle

    # move to low position
    # sliding start point
    curr1 = 271
    curr2 = 1400
    curr3 = 309
    curr4 = 2324

    # move to starting position
    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1)
    reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2)
    reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr3)
    reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4)
    time.sleep(3)

    # check horizontally for sliding object
    found = Check_Horizontal(curr1)

    # tap object
    if found:
        reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 + 200)
        reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr4 - 200)
        time.sleep(1)
        reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 100)
        time.sleep(1)
        while True:
            [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
            print(dxl2_current)
            if dxl2_current >= 0:
                newcurr2 = reader.Read_Value(motors[1], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
                newcurr4 = reader.Read_Value(motors[3], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)

                reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr2 - 1)
                reader.Set_Value(motors[3], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr4 + 1)

                print("Object detected")
                time.sleep(1)

                break
        tap_object(reader)

    # side tap object
    if found:
        newcurr3 = curr3
        reader.Set_Value(motors[2], ADDR_PRO_VELOCITY, LEN_PRO_VELOCITY, 25)
        for taps in range(3):
            minreading = 1
            reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr3 - 150)
            # time.sleep(0.25)
            for repetitions in range(50):
                [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
                if dxl3_current < minreading:
                    minreading = dxl3_current
            newcurr3 -= 25
            reader.Set_Value(motors[2], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr3)
            time.sleep(0.25)

    # slide object
    if found:
        # sliding inverted start point
        curr1 = 301
        curr2 = 1550
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

        N_QUERIES = 200

        for queries in range(N_QUERIES):
            dxl1_current = reader.Read_Sync_Once()[1]
            # print(dxl1_current)
            if dxl1_current < -500:
                print("Object is immovable!")
                curr = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
                reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr)
                break
            elif dxl1_current > -10:
                print("Object has tipped over or is out of position!")
                curr = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
                reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr)
                break
            elif -75 > dxl1_current > lastreading > secondtolast:
                print("Object is undergoing static friction!")
            elif dxl1_current < -100:
                print("Object is moving!")

            secondtolast = lastreading
            lastreading = dxl1_current

        time.sleep(2)
        reader.Set_Value(motors[1], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr2 - 700)
        time.sleep(3)

    # print what object is (foam vs battery vs toolbox)

    del reader
