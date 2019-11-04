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
    # curr2 = 1200
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

    time.sleep(5)
    print("Ready to interrogate.")

    reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, curr1 - 600)
    time.sleep(0.25)

    # # determining whether and object is immobile or not
    # while True:
    #     if reader.Read_Sync_Once()[1] <= -500:
    #         newcurr1 = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    #         reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr1)
    #         print("Object is immovable")
    #         break

    # # for detecting an object
    # while True:
    #     if reader.Read_Sync_Once()[1] <= -20:
    #         newcurr1 = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    #         reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr1)
    #         print("Object detected")
    #         break

    # # for gathering data on an object tipped over
    # fname = "tippedovertissue_markerslides.csv"
    # fout = open(fname, "w")
    # print("Timestamp, Current1, Current2, Current3, Current4", file=fout)
    # while reader.Read_Value(motors[0], ADDR_MOVING, LEN_MOVING):
    #     [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
    #     print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
    #           file=fout)
    # fout.close()

    # # # detecting whether an object tips over
    # while True:
    #     dxl1_current = reader.Read_Sync_Once()[1]
    #     print(dxl1_current)
    #     if dxl1_current <= -20:
    #         print("Object detected")
    #         break
    # while True:
    #     dxl1_current = reader.Read_Sync_Once()[1]
    #     print(dxl1_current)
    #     if dxl1_current >= -10:
    #         newcurr1 = reader.Read_Value(motors[0], ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    #         reader.Set_Value(motors[0], ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, newcurr1)
    #         print("Object tipped over")
    #         break
    #
    # for gathering data on and detecting an object sliding
    fname = "slidingtoolbox_markerslides.csv"
    fout = open(fname, "w")
    print("Timestamp, Current1, Current2, Current3, Current4", file=fout)
    while reader.Read_Value(motors[0], ADDR_MOVING, LEN_MOVING):
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()
        # print("%09d,%05d,%05d,%05d,%05d" % (timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current),
        #       file=fout)
        if dxl1_current < -50:
            print("Object is currently sliding")
    fout.close()

    time.sleep(3)
    del reader
