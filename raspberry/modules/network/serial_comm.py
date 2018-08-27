# Serial communication with STM32.

# Import modules
import serial # Serial communication package
sys.path.insert(0,'..') # Go parent directory
from logging import * # Import logging module
from colors import * # Import colored print module

# Data format which is coming from raspberry pi
# [gain, x, y, z, roll, pitch, yaw, gripper]

# Data format which will send to raspberry pi
# [rov_state, temp, pressure, leak_info]

class Serial(object):
    def __init__(self,port,baudrate=9600,timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.send_data = ""
        self.recv_data = ""
        info("Port: " + self.port + "\n"
           + "Baudrate: " + str(self.baudrate) + "\n"
           + "Timeout: " + str(self.timeout))
        success("Serial connection created")

    def connect(self):
        count = 0;
        while True:
            try:
                count += 1
                server_serial = serial.Serial(port=self.port,
                                              baudrate = self.baudrate,
                                              parity=serial.PARITY_NONE,
                                              stopbits=serial.STOPBITS_ONE,
                                              bytesize=serial.EIGHTBITS,
                                              timeout=self.timeout)
                success("Connection established")
                break
            except: # Probably TimeoutError
                if(count <= 3):
                    error("Port is not responding")
                    wait("Trying to connect again...")
                    underline("Attempt: " + str(count))
                else:
                    error("Connection failed after 3 attempts")
                    break
