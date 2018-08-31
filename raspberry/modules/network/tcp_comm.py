# Communication with Ground station using TCP

# Import modules
import socket # TCP communication package
import sys
sys.path.insert(0,'..') # Go parent directory
from logging import * # Import logging module
from colors import * # Import colored print module
import exceptions

class TCP(object):
    def __init__(self, server_ip, port, buffer_size=4096):
        self.client_ip = socket.gethostbyname(socket.gethostname()) # Get Host IP
        self.server_ip = server_ip
        self.port = port
        self.buffer_size = buffer_size # bits
        self.send_data = ""
        self.recv_data = ""
        info("Client IP: " + self.client_ip + "\n"
           + "Server IP: " + self.server_ip + "\n"
           + "Port: " + str(self.port) + "\n"
           + "Buffer Size: " + str(self.buffer_size))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
        self.client_socket.settimeout(30) # 30 seconds timeout
        success("Socket created")

    def getSocketInfo(self): # Return dictionary
        return {"Client IP" : self.client_ip,
                "Server IP" : self.server_ip,
                "Port" : self.port,
                "Buffer Size" : self.buffer_size}

    def connect(self):
        count = 0;
        while True:
            try:
                count += 1
                self.client_socket.connect((self.server_ip, self.port)) # Try to connect
                success("TCP connection established to " + self.server_ip + ":" + str(self.port))
                break
            except TimeoutError:
                if(count <= 3):
                    error(exceptions.server)
                    wait("Trying to connect again...")
                    underline("Attempt: " + str(count))
                else:
                    error(exceptions.attempts)
                    break
            except OSError:
                error(exceptions.no_connect)
                break

    def send(self, temp, pressure):
        try:
            self.send_data = "rov" + "-" + "base" + "-" + str(timestamp()) + "-" + str(temp) + "-" +  str(pressure) # Fill send_data format
            packet = str.encode(self.send_data) # Encode string to bytes
            self.client_socket.sendall(packet) # Send data to base
            info("Sending Data to base: " + self.send_data)
        except:
            error(exceptions.send)

    def recv(self):
        try:
            self.recv_data = self.client_socket.recv(self.buffer_size) # Fill recv_data with coming data
            info("Receiving Data from base: " + self.recv_data)
            return str(self.recv_data)
        except:
            error(exceptions.recv)

    def failure(self, problem): # Leak detected, Motor down, Crashed...
        try:
            self.client_socket.sendall(str.encode("FAILURE: " + problem))
            error(bold("FAILURE: ROV will disarm automatically\t") + underline(problem))
        except:
            error(exceptions.fatal)

    def send_info(self, type, info): # Leak detected, Motor down, Crashed...
        try:
            self.client_socket.sendall(str.encode(info))
            success(bold(underline("Send " + type + " info")))
        except:
            error("Cannot send " + type + "info")

    def kill(self):
        reset_terminal()
        warn("TCP connection will be terminated. Would you like to proceed? [Yes/No]:\t")
        answer = input()
        if(answer.lower().startswith("y"))
            self.client_socket.close()
            info("TCP Connection terminated")
