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
