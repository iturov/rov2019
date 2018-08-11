# Communication with Ground station using TCP

# Import modules
import socket
import sys
sys.path.insert(0,'..') # Go parent directory
from logging import * # Import logging module
from colors import * # Import colored print module

# Data which is coming from groundstation.
# [source_id, destination_id, timestamp, x, y, z, roll, pitch, yaw, temp, pressure, gripper]

class Client(object):
    def __init__(self, server_ip, port, buffer_size=1024):
        self.client_ip = socket.gethostbyname(socket.gethostname()) # Get Host IP
        self.server_ip = server_ip
        self.port = port
        self.buffer_size = buffer_size
        info("Client IP: " + self.client_ip + "\n"
           + "Server IP: " + self.server_ip + "\n"
           + "Port: " + self.port + "\n"
           + "Buffer Size: " + self.buffer_size)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
        self.client_socket.settimeout(30) # 30 seconds timeout
        success("Socket created")

    def connect(self):
        count = 0;
        while True:
            try:
                count += 1
                self.client_socket.connect((self.server_ip,self.port)) # Try to connect
                success("Connection established")
                log("Connection established to " + self.server_ip + ":" + self.port)
                break
            except TimeoutError:
                if(count <= 3):
                    error("ERROR: Server is not responding")
                    log("ERROR: Server is not responding")
                    wait("Trying to connect again...")
                    underline("Attempt: " + str(count))
                else:
                    error("ERROR: Connection failed after 3 attempts")
                    log("ERROR: Connection failed after 3 attempts")
                    break
            except OSError:
                error("ERROR: No Connection found")
                log("ERROR: No Connection found")
                break
