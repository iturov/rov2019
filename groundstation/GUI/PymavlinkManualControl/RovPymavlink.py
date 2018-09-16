from pymavlink import mavutil
import time

def listAvailableMods(master):
    print('Available Mods: ', list(master.mode_mapping().keys()))
    # List Available Mods

def modeChange(master, modeName):
    print("** Mode changed to: {} **".format(modeName))
    mode_id = master.mode_mapping()[modeName]
    master.set_mode(mode_id)
    # Change the mode to 'modeName'

def rovMove(master, xVelo, yVelo, zVelo):
    master.mav.manual_control_send(master.target_system, xVelo, 0, yVelo,zVelo,1)

def readInfo(master, msgType):
    # msgType should be string
    msg = master.recv_match()
    if not msg:
        return "0"

    if msg.get_type() == msgType:
        return msg

# Starts Connection
master = mavutil.mavlink_connection('udp:192.168.2.1:14550')
# Wait for vehicle to send a heartbeat,Very Important !
master.wait_heartbeat()
# Send our first heartbeat. Not sure if its neccessary for setting mode, didn't try it yet.
master.mav.heartbeat_send(6,8,192,0,4,3)
# Arm the vehicle
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)

while True:
    # We should send heartbeats at most 1 second interval, less is doing fine.
    master.mav.heartbeat_send(6,8,192,0,4,3)
    # Set the velocity for axis (x,y,z) (Normally limits of axis are from -1000 to 1000 but z axis is working on 0 to 1000 interval so 500 is the middle value)
    rovMove(master, 0, 500, 0)
    # Print the pressure values
    msg = master.recv_match()
    if not msg:
        continue
    if msg.get_type() == 'SCALED_IMU2':
        print(msg)