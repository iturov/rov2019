# Communication with Ground station using TCP

# Import modules
import socket
import sys
sys.path.insert(0,'..') # Go parent directory
from logging import * # Import logging module
from colors import * # Import colored print module

# Special commands
# arm, disarm

# Data format which is coming from ground station.
# [source_id, destination_id, timestamp, gain, x, y, z, roll, pitch, yaw, gripper]

# Data format which will send to ground station
# [source_id, destination_id, timestamp, temp, pressure]

class Client(object):
    def __init__(self, server_ip, port, buffer_size=1024):
        self.client_ip = socket.gethostbyname(socket.gethostname()) # Get Host IP
        self.server_ip = server_ip
        self.port = port
        self.buffer_size = buffer_size
        self.send_data = ""
        self.recv_data = ""
        info("Client IP: " + self.client_ip + "\n"
           + "Server IP: " + self.server_ip + "\n"
           + "Port: " + str(self.port) + "\n"
           + "Buffer Size: " + str(self.buffer_size))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
        self.client_socket.settimeout(30) # 30 seconds timeout
        success("Socket created")

    def getSocketInfo(self):
        return("Client IP: " + self.client_ip + "\n"
           + "Server IP: " + self.server_ip + "\n"
           + "Port: " + str(self.port) + "\n"
           + "Buffer Size: " + str(self.buffer_size))

    def connect(self):
        count = 0;
        while True:
            try:
                count += 1
                self.client_socket.connect((self.server_ip, self.port)) # Try to connect
                success("Connection established to " + self.server_ip + ":" + str(self.port))
                break
            except TimeoutError:
                if(count <= 3):
                    error("ERROR: Server is not responding")
                    wait("Trying to connect again...")
                    underline("Attempt: " + str(count))
                else:
                    error("ERROR: Connection failed after 3 attempts")
                    break
            except OSError:
                error("ERROR: No Connection found")
                break

    def send(self, temp, pressure):
        try:
            self.send_data = str(["rov", "base", timestamp(), temp, pressure]) # Fill send_data format
            packet = str.encode(self.send_data) # Encode string to bytes
            self.client_socket.send(packet) # Send data to server
            info("Sending Data: " + self.send_data)
        except:
            error("Error occured while sending data")

    def recv(self):
        try:
            self.recv_data = self.client_socket.recv(self.buffer_size) # Fill recv_data with coming data
            info("Receiving Data: " + self.recv_data)
            return str(self.recv_data)
        except:
            error("Error occured while receiving data")

    def failure(self):
        try:
            self.client_socket.send("failure")
            warn("Problem detected! ROV will disarm automatically")
        except:
            error("Fatal error")

    def kill(self):
        self.client_socket.close()
        warn("Connection killed")
