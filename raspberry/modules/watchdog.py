from logging import * # Import logging module
from colors import * # Import colored print module
import os
import exceptions

def checkBaseState(host):
    state = os.system('ping {} {} > /dev/null'.format("-c 1", host)) == 0
    if(state):
        return state
    else:
        error(exceptions.tcp_fail)
        exit()
def checkStmState(port):
    try:
        test_connection = serial.Serial(port)
        test_connection.close()
        del test_connection
        return True
    except:
        error(exceptions.serial_fail)
        exit()
