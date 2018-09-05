# Special commands
# arm, disarm, failure...

# Data format which is coming from ground station and sending to STM32.
# [source_id, destination_id, timestamp, x, y, z, roll, pitch, yaw, gripper]

# Data format which will receive from STM32 and send to ground station
# [source_id, destination_id, timestamp, temp, pressure]

# IDs: "base" - "rov" - "stm"

# 3 Services working simultaneously

# Import modules
from logging import * # Import logging module
from colors import * # Import colored print module
from watchdog import * # Import system watchdog
from network.serial_comm import *
from network.tcp_comm import *
from multiprocessing import Process

# loop1
def systemLoop(): # Check system state every minute
    success("Watchdog is running")
    while(True):
        checkBaseState(tcpClient.server_ip)
        checkStmState(stmServer.port)
        time.sleep(60)

# loop2
def serialLoop():
    stmServer.connect()
    while(True):
        coming_data = tcpClient.recv()
        coming_array = list(coming_data.split("-"))
        if(len(coming_array) =! 2): # It must be a failure
            try:
                tcpClient.failure(problem = coming_array[0])
            except:
                error("Error while sending data to groundstation")
        else:
            try:
                tcpClient.send(temp = coming_array[0],
                               pressure = coming_array[1])
            except:
                error("Error while sending data to groundstation")

# loop3
def tcpLoop():
    tcpClient.connect()
    while(True):
        coming_data = tcpClient.recv()
        coming_array = list(coming_data.split("-"))
        if(len(coming_array) =! 11):
            try:
                if(coming_array[3] == "ARM"):
                    stmServer.arm()
                elif(coming_array[3] == "DISARM"):
                    stmServer.disarm()
                elif(coming_array[3][:4] == "SET_GAIN"):
                    stmServer.set_gain(value = float(coming_array[3][5:]))
                elif(coming_array[3] == "GET_SERIAL_INFO"):
                    tcpClient.send_info(type="serial", info=str(stmServer.getSerialInfo())
                elif(coming_array[3] == "GET_TCP_INFO"):
                    tcpClient.send_info(type="TCP", info=str(tcpClient.getSocketInfo())
                elif(coming_array[3] == "KILL_CONNECTION"):
                    tcpClient.kill()
            except:
                error("Error while reading coming data from ground station")
        else
            try:
                stmServer.send(x = coming_array[3],
                               y = coming_array[4],
                               z = coming_array[5],
                               roll = coming_array[6],
                               pitch = coming_array[7],
                               yaw = coming_array[8],
                               gripper = coming_array[9])
            except:
                error("Error while sending data to STM32")

# System Started
success(bold("System Started"))

# Create communication objects
stmServer = Serial(port='/dev/ttyUSB0')
tcpClient = TCP(server_ip='192.168.2.1', port='1864')

# Start services
Process(target=systemLoop).start() # General system loop
Process(target=serialLoop).start() # Serial recv loop
Process(target=tcpLoop).start() # TCP recv loop
