#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 12:50:09 2019

@author: Jason Ah Chuen, Ante Qu

Arm keeps moving in the specified direction until an obstacle (constant event) is hit.
Prints position of obstacle

"""

from CurrentReader import *
import numpy as np
from scipy.signal import butter, lfilter, freqz
import time

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def run_filter(data, b, a):
    y = lfilter(b, a, data)
    return y

def get_motor():
    
    global reader
    # Decide which joint to move
    joint = int(input("Enter 1 for joint 1. Enter 2 for joint 2: "))
    
    global direction
    # Decide which direction to move
    direction = str(input("Enter l for left direction, r for right direction, u for up direction, d for down direction: "))
    
    # Decide which joint to move
    if joint == 1:
        if direction == 'l' or direction == 'r':
            return reader.m1id
        elif direction == 'u' or direction == 'd':
            return reader.m2id
    elif joint == 2:
        if direction == 'l' or direction == 'r':
            return reader.m3id
        elif direction == 'u' or direction == 'd':
            return reader.m4id
    else:
        print("Inappropriate input. EXIT")
        del reader
        sys.exit(0)
        

if __name__ == '__main__':

    reader = DynamixelReader()

    ADDR_PRO_GOAL_POSITION = 116
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4
    LEN_PRO_PRESENT_POSITION = 4
    motors = [reader.m1id, reader.m2id, reader.m3id, reader.m4id]

    N_QUERIES = 10000000

    # move to start position
    # # set lower velocity limit, maybe not necessary
    # ADDR_VELO_LIMIT = 44
    # LEN_VELO_LIMIT = 4
    # for motor in motors:
    #     reader.Set_Value(motor, ADDR_VELO_LIMIT, LEN_VELO_LIMIT, 100)

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
    reader.Set_Value(reader.m1id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 308)
    reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 901)
    reader.Set_Value(reader.m3id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 311)
    reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, 2775)

    # read initial position
    current_position2 = 901
    current_position4 = 2775
    
    # Array of readings initialized to 0
    x = np.zeros((N_QUERIES,))
    y = np.zeros((N_QUERIES,))
    
    # Array for event detection
    numzeros = 5
    e = np.zeros(numzeros)
    
    # Number of consecutive events detected
    num_event = 0
    
    timestamp = 0
    fs = 240.
    low = 5.
    hi = 100.
    b, a = butter_bandpass(low, hi, fs, order=4)
    M = b.size
    N = a.size
    j = 0

    print("Ready to read.")

    time.sleep(3)

    while 1:
        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        # # compute norm
        # x[j] = np.sqrt(dxl1_current**2 + dxl2_current**2 + dxl3_current**2 + dxl4_current**2)
        #
        # filter
        # if j < numzeros:
        #     if j >= (numzeros / 2):
        #         # filter everything using lfilter
        #         y[0:j+1] = lfilter(b, a, x[0:j+1])
        # else:
        #     y[j] = 1./a[0] * (b.dot(x[j:j-M:-1]) - a[1:N].dot(y[j-1:j-N:-1]))
        #
        # # Event detection. Stop if object is detected. Keep moving arm if no object is detected
        # if np.abs(y[j]) > 1. and np.abs(y[j-1]) > 1.:
        #     # print(" EVENT ")
        #
        #     # To make sure that event is constant and not just a fluctuation
        #     if e[numzeros - 1] == 1:
        #         print("Object detected")
        #         print(current_position2 - int(j))
        #         break
        #     else:
        #         e[num_event] = 1
        #         num_event += 1
        if dxl2_current > 10:
            num_event += 1
            if num_event == numzeros:
                print("Object detected")
                break
        else:
            # Reset array for event detection
            # e = np.zeros(numzeros)
            # num_event = 0

            # reset
            num_event = 0
            
            reader.Set_Value(reader.m2id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position2 + int(j))
            reader.Set_Value(reader.m4id, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position4 - int(j))
        
        difft = timestamp - oldtimestamp
        # print("%09d,%f" % (timestamp, y[j] ))
        j += 1
    del reader
