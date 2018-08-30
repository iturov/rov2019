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
    def __init__(self,port,baudrate=115200,read_timeout=5.0, write_timeout=5.0, buffer_size=4):
        self.port = port
        self.baudrate = baudrate
        self.read_timeout = read_timeout # seconds
        self.write_timeout = write_timeout # seconds
        self.buffer_size = buffer_size # bytes
        self.send_data = ""
        self.recv_data = ""
        info("Port: " + self.port + "\n"
           + "Baudrate: " + str(self.baudrate))
        success("Serial connection created")

    def getSerialInfo(self): # Return dictionary
        return {"Port" : self.port,
                "Baudrate" : self.baudrate,
                "Read Timeout" : self.read_timeout,
                "Write Timeout" : self.write_timeout}

    def connect(self):
        count = 0;
        while True:
            try:
                count += 1
                self.server_serial = serial.Serial(port=self.port,
                                              baudrate = self.baudrate,
                                              parity=serial.PARITY_NONE,
                                              stopbits=serial.STOPBITS_ONE,
                                              bytesize=serial.EIGHTBITS,
                                              timeout=self.timeout
                                              write_timeout=self.write_timeout)
                success("Connection established")
                break
            except SerialException:
                if(count <= 3):
                    error("Port is not responding")
                    wait("Trying to connect again...")
                    underline("Attempt: " + str(count))
                else:
                    error("Connection failed after 3 attempts")
                    break

    def send(self, gain, x, y, z, roll, pitch, yaw, gripper):
        try:
            self.send_data = str(["rov", "stm", timestamp(), gain, x, y, z, roll, pitch, yaw, gripper]) # Fill send_data format
            packet = str.encode(self.send_data) # Encode string to bytes
            self.server_serial.write(packet) # Send data to stm
            info("Sending Data to stm: " + self.send_data)
        except: # SerialTimeoutException
            error("Error occured while sending data")

    def recv(self):
        try:
            self.recv_data = self.server_serial.read_until(size=self.buffer_size) # Fill recv_data with coming data
            info("Receiving Data from base: " + self.recv_data)
            return str(self.recv_data)
        except:
            error("Error occured while receiving data")

    def kill(self):
        reset_terminal()
        if(slef.server_serial.is_open()):
            warn("Serial connection will be terminated. Would you like to proceed? [Yes/No]:\t")
            answer = input()
            if(answer.lower().startswith("y"))
                self.server_serial.close()
                info("Serial Connection terminated")

    def arm(self):
        self.server_serial.write(str.encode("ARM"))
        success(bold(underline("Armed")))

    def disarm(self):
        self.server_serial.write(str.encode("DISARM"))
        success(bold(underline("Disarmed")))
