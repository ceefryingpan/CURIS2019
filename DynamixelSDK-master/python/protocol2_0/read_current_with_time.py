#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)
# modified by Ante Qu

#
# *********     Bulk Read and Bulk Write Example      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using two Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(support.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 and 2 / Baudnum : 1 (Baudrate : 57600)
#

import os, ctypes

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

os.sys.path.append('../dynamixel_functions_py')             # Path setting

import dynamixel_functions as dynamixel                     # Uses Dynamixel SDK library
import datetime

N_QUERIES                    = 1000
OUT_STEP                     = 1
# Control table address
ADDR_PRO_TORQUE_ENABLE       = 64                          # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION       = 116
ADDR_PRO_REALTIME_TICK       = 120
ADDR_PRO_PRESENT_POSITION    = 132
ADDR_PRO_LED_RED             = 65

# Data Byte Length
LEN_PRO_GOAL_POSITION       = 4
LEN_PRO_PRESENT_POSITION    = 4
LEN_PRO_REALTIME_TICK       = 2
LEN_PRO_LED_RED             = 1

# Protocol version
PROTOCOL_VERSION            = 2                             # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID                     = 101                             # Dynamixel ID: 1
DXL2_ID                     = 103                             # Dynamixel ID: 2
BAUDRATE                    = 1000000
DEVICENAME                  = "COM5".encode('utf-8')# Check which port is being used on your controller
                                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = -150                          # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  =  150                          # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                            # Dynamixel moving status threshold

ESC_ASCII_VALUE             = 0x20

COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed


# Initialize PortHandler Structs
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
port_num = dynamixel.portHandler(DEVICENAME)

# Initialize PacketHandler Structs
dynamixel.packetHandler()

# Initialize groupBulkWrite Struct
groupwrite_num = dynamixel.groupBulkWrite(port_num, PROTOCOL_VERSION)

# Initialize Groupsyncwrite instance
groupread_num = dynamixel.groupBulkRead(port_num, PROTOCOL_VERSION)

index = 0
dxl_comm_result = COMM_TX_FAIL                              # Communication result
dxl_addparam_result = 0                                     # AddParam result
dxl_getdata_result = 0                                      # GetParam result
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position

dxl_error = 0                                               # Dynamixel error
dxl_led_value = [0, 1]                                    # Dynamixel LED value for write
dxl1_present_position = 0                                   # Present position
dxl2_led_value_read = 0                                     # Dynamixel moving status
dxl1_realtime_tick = 0

# Open port
if dynamixel.openPort(port_num):
    print("Succeeded to open the port!")
else:
    print("Failed to open the port!")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if dynamixel.setBaudRate(port_num, BAUDRATE):
    print("Succeeded to change the baudrate!")
else:
    print("Failed to change the baudrate!")
    print("Press any key to terminate...")
    getch()
    quit()


# Enable Dynamixel#1 Torque
dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
if dxl_comm_result != COMM_SUCCESS:
    print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
elif dxl_error != 0:
    print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
else:
    print("Dynamixel#1 has been successfully connected")

dxl1_present_position = dynamixel.read4ByteTxRx(port_num, PROTOCOL_VERSION, DXL1_ID, ADDR_PRO_PRESENT_POSITION)
dxl_goal_position = [dxl1_present_position + DXL_MINIMUM_POSITION_VALUE, dxl1_present_position + DXL_MAXIMUM_POSITION_VALUE]

# Enable Dynamixel#2 Torque
dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
if dxl_comm_result != COMM_SUCCESS:
    print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
elif dxl_error != 0:
    print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))
else:
    print("Dynamixel#2 has been successfully connected")


# Add parameter storage for Dynamixel#1 present position value
dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupBulkReadAddParam(groupread_num, DXL1_ID, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)).value
if dxl_addparam_result != 1:
    print("[ID:%03d] groupBulkRead addparam failed - present position" % (DXL1_ID))
    quit()


# Add parameter storage for Dynamixel#2 present moving value
dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupBulkReadAddParam(groupread_num, DXL2_ID, ADDR_PRO_LED_RED, LEN_PRO_LED_RED)).value
if dxl_addparam_result != 1:
    print("[ID:%03d] groupBulkRead addparam failed - LED" % (DXL2_ID))
    quit()


# TODO ANTE: Change this to a for loop
#for j in range(N_QUERIES):
while 1:
    print("Press any key to continue! (or press SPACE to quit!)")
    if getch() == chr(ESC_ASCII_VALUE):
        break

    # Add parameter storage for Dynamixel#1 goal position
    dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupBulkWriteAddParam(groupwrite_num, DXL1_ID, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION, dxl_goal_position[index], LEN_PRO_GOAL_POSITION)).value
    if dxl_addparam_result != 1:
        print("[ID:%03d] groupBulkWrite addparam failed" %(DXL1_ID), file=sys.stderr)
        quit()

    # Add parameter storage for Dynamixel#2 LED value
    dxl_addparam_result = ctypes.c_ubyte(dynamixel.groupBulkWriteAddParam(groupwrite_num, DXL2_ID, ADDR_PRO_LED_RED, LEN_PRO_LED_RED, dxl_led_value[index], LEN_PRO_LED_RED)).value
    if dxl_addparam_result != 1:
        print("[ID:%03d] groupBulkWrite addparam failed" %(DXL2_ID), file=sys.stderr)
        quit()

    # Bulkwrite goal position and LED value
    dynamixel.groupBulkWriteTxPacket(groupwrite_num)
    dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    if dxl_comm_result != COMM_SUCCESS:
        print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))

    # Clear bulkwrite parameter storage
    dynamixel.groupBulkWriteClearParam(groupwrite_num)

    while 1:
        # Bulkread realtime tick, present position, and moving status
        dynamixel.groupBulkReadTxRxPacket(groupread_num)
        dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
        if dxl_comm_result != COMM_SUCCESS:
            print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))

        # Check if groupbulkread data of Dynamixel#1 is available
        dxl_getdata_result = ctypes.c_ubyte(dynamixel.groupBulkReadIsAvailable(groupread_num, DXL1_ID, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)).value
        if dxl_getdata_result != 1:
            print("[ID:%03d] groupBulkRead getdata failed present position: %d" % (DXL1_ID, dxl_getdata_result))
            quit()

        # Check if groupbulkread data of Dynamixel#2 is available
        dxl_getdata_result = ctypes.c_ubyte(dynamixel.groupBulkReadIsAvailable(groupread_num, DXL2_ID, ADDR_PRO_LED_RED, LEN_PRO_LED_RED)).value
        if dxl_getdata_result != 1:
            print("[ID:%03d] groupBulkRead getdata failed LED" % (DXL2_ID))
            quit()

        # Get Dynamixel#1 present position value
        dxl1_present_position = dynamixel.groupBulkReadGetData(groupread_num, DXL1_ID, ADDR_PRO_PRESENT_POSITION, LEN_PRO_PRESENT_POSITION)

        # Get Dynamixel#2 moving status value
        dxl2_led_value_read = dynamixel.groupBulkReadGetData(groupread_num, DXL2_ID, ADDR_PRO_LED_RED, LEN_PRO_LED_RED)

        currentTimeuS = datetime.datetime.now().microsecond
        print("[ID:%03d] Present Position: %d \t [ID:%03d] LED Value: %d \t Local time: %d" % (DXL1_ID, dxl1_present_position,
                                                                                DXL2_ID, dxl2_led_value_read, currentTimeuS))

        if not (abs(dxl_goal_position[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD):
            break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0


# Disable Dynamixel#1 Torque
dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
if dxl_comm_result != COMM_SUCCESS:
    print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
elif dxl_error != 0:
    print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

# Disable Dynamixel#2 Torque
dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
dxl_error = dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION)
if dxl_comm_result != COMM_SUCCESS:
    print(dynamixel.getTxRxResult(PROTOCOL_VERSION, dxl_comm_result))
elif dxl_error != 0:
    print(dynamixel.getRxPacketError(PROTOCOL_VERSION, dxl_error))

# Close port
dynamixel.closePort(port_num)
