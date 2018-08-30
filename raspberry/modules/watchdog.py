from logging import * # Import logging module
from colors import * # Import colored print module
import subprocess

def checkBaseState(ip_address):
    text = str(subprocess.Popen(["/bin/ping", "-c1", ip_address], stdout=subprocess.PIPE).stdout.read())
    start_index = text.find("time=") + 5
    stop_index = text.find("ms") + 2
    ping = text[start_index:stop_index]
    if(ping.find("error") =! -1):
        error("TCP connection failed. System will be terminated")
        exit()
    else:
        return ping

def checkStmState(port):
    try:
        test_connection = serial.Serial(port)
        test_connection.close()
        del test_connection
        return True
    except:
        error("Serial connection failed. System will be terminated")
        exit()
