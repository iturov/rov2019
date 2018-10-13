from logging import * # Import logging module
from colors import * # Import colored print module

class exceptions():
    # serial_comm exceptions
    port = "Port is not responding"
    arm = "Cannot armed"
    disarm = "Cannot disarmed"
    gain = "Cannot set gain"
    serial_fail = "Serial connection failed. System will be terminated"
    serial_send = "Error while sending data to STM32"
    serial_recv = "Error while reading coming data from STM32"
    # tcp_comm exceptions
    server = "Server is not responding"
    no_connect = "No Connection found"
    tcp_fail = "TCP connection failed. System will be terminated"
    tcp_send = "Error while sending data to groundstation"
    tcp_recv = "Error while reading coming data from ground station"

    # common exceptions
    send = "Error occured while sending data"
    recv = "Error occured while receiving data"
    attemps = "Connection failed after 3 attempts"
    fatal = "Fatal error"
