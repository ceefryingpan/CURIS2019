#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 12:50:09 2019

@author: jasonahchuen

Arm keeps moving in the specified direction until an obstacle is hit

"""

from CurrentReader import *
import numpy as np
from scipy.signal import butter, lfilter, freqz



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

    reader = DynamixelReader(device_name = "/dev/tty.usbserial-FT2N0DM5".encode('utf-8'),
                             # baud rate
                             baud_rate = 115200,
                             # motor ids
                             m1id = 100, m2id = 101, m3id = 102, m4id = 103,
                             # protocol ver
                             proto_ver = 2,
                             # Motor Current Addr and Len
                             read_addr = 126, read_len = 2)

    ADDR_PRO_GOAL_POSITION = 116
    ADDR_PRO_PRESENT_POSITION = 132
    LEN_PRO_GOAL_POSITION = 4
    LEN_PRO_PRESENT_POSITION = 4
    
    #motor = get_motor()
    
    
    # Decide which joint to move
    joint = int(input("Enter 1 for joint 1. Enter 2 for joint 2: "))
    
    # Decide which direction to move
    direction = str(input("Enter l for left direction, r for right direction, u for up direction, d for down direction: "))
    
    # Decide which joint to move
    if joint == 1:
        if direction == 'l' or direction == 'r':
            motor = reader.m1id
        elif direction == 'u' or direction == 'd':
            motor = reader.m2id
    elif joint == 2:
        if direction == 'l' or direction == 'r':
            motor = reader.m3id
        elif direction == 'u' or direction == 'd':
            motor = reader.m4id
    else:
        print("Inappropriate input. EXIT")
        del reader
        sys.exit(0)
    
    N_QUERIES = 10000000
    
    #Reading current position at start
    current_position = reader.Read_Value(motor, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)
    
    # Array of readings initialized to 0
    x = np.zeros((N_QUERIES,))
    y = np.zeros((N_QUERIES,))
    
    timestamp = 0
    fs = 240.
    low = 5.
    hi = 100.
    b,a = butter_bandpass(low,hi,fs, order=4)
    M=b.size
    N=a.size
    j = 0;
    
    while 1:
        print("here")
        oldtimestamp = timestamp

        # read all current
        [timestamp, dxl1_current, dxl2_current, dxl3_current, dxl4_current] = reader.Read_Sync_Once()

        # compute norm
        x[j] = np.sqrt(dxl1_current**2 + dxl2_current**2 + dxl3_current**2 + dxl4_current**2)
        #filter
        if (j < 20):
            if (j>= 10):
                # filter everything using lfilter
                y[0:j+1]= lfilter(b, a, x[0:j+1])
            else:
                # don't filter first ten
                y[j] = x[j]
        else:
            y[j] = 1./a[0] *( b.dot(x[j:j-M:-1]) - a[1:N].dot(y[j-1:j-N:-1]))
        if (np.abs(y[j]) > 1. and np.abs(y[j-1]) > 1.):
            print( " EVENT ")
            #if (repeated EVENT)
                #break
        else:
            skip = 10
            if j % skip == 0:
                if (direction == 'l' or direction == 'u'):
                    reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position - int(j/10))
                else:
                    reader.Set_Value(motor, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, current_position + int(j/10))
        j += 1
        difft = timestamp - oldtimestamp
        print("%09d,%f" % (timestamp, y[j] ))
    del reader
