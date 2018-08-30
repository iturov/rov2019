# Special commands
# arm, disarm, leak_detected ...

# Data format which is coming from ground station and sending to STM32.
# [source_id, destination_id, timestamp, gain, x, y, z, roll, pitch, yaw, gripper]

# Data format which will receive from STM32 and send to ground station
# [source_id, destination_id, timestamp, temp, pressure]

# IDs: "base" - "rov" - "stm"

# There will be 2 threads working simultaneously

# loop1
while(True):
    tcp_data = TCPClient.recv()
    serial_data = convertToSerialFormat(tcp_data)
    SerialServer.send(serial_data)

# loop2
while(True):
    serial_data = SerialServer.recv()
    tcp_data = convertToTCPFormat(serial_data)
    TCPClient.send(tcp_data)

# conditions
if(tcp_data[command_index] == "arm"):
    SerialServer.arm()

elif(tcp_data[command_index] == "disarm"):
    SerialServer.disarm()
